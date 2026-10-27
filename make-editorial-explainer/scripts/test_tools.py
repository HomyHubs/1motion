#!/usr/bin/env python3
"""Local helper tests. Integration uses synthetic tone/colour, not VieNeu or a motion renderer."""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import project_tools as t

class Helpers(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'pilot'
        t.init(self.root)
        shutil.copyfile(t.ROOT/'examples/pilot.project.json',self.root/'project.json');self.doc=t.load(self.root)
    def tearDown(self): self.tmp.cleanup()
    def test_example(self): self.assertEqual(t.validate(self.doc,self.root),[])
    def test_init_is_blank(self):
        blank=Path(self.tmp.name)/'blank';t.init(blank);doc=t.load(blank)
        self.assertEqual([doc['sources'],doc['claims'],doc['assets'],doc['beats']],[[],[],[],[]])
        self.assertEqual(sorted(t.validate(doc,blank)),['At least one beat required','Empty title'])
        self.assertNotIn('runtime',json.loads((blank/'capabilities.json').read_text(encoding='utf-8')))
    def test_doctor_honors_env_overrides(self):
        fake=self.root/'fake-python'
        fake.write_text('',encoding='utf-8')
        with mock.patch.dict(os.environ,{'VIENEU_PYTHON':str(fake),'VIENEU_VOICE':'v1','HYPERFRAMES_CMD':'hf-cmd'}):
            report=t.doctor()
        self.assertEqual((report['vieneu_python'],report['vieneu_python_exists'],report['vieneu_voice'],report['tools']['hyperframes']),(str(fake),True,'v1','hf-cmd'))
        self.assertEqual(report['tools']['python'],sys.executable)
        self.assertIn(report['os'], ('nt', 'posix'))
        self.assertGreater(report['disk_free_gb'], 0)
    def test_voice_requires_vieneu_interpreter(self):
        with mock.patch.dict(os.environ,{'VIENEU_PYTHON':str(self.root/'missing-python')}):
            with self.assertRaisesRegex(ValueError,'VieNeu interpreter not found'): t.voice(self.root,[])
    def test_refuse_existing(self):
        with self.assertRaises(ValueError): t.init(self.root)
    def test_duplicate_and_unknown(self):
        self.doc['beats'][1]['id']='01'
        self.assertTrue(any('Duplicate' in e for e in t.validate(self.doc,self.root)))
        self.doc['beats'][1]['id']='02';self.doc['beats'][0]['claim_ids']=['fake']
        self.assertTrue(any('Unknown' in e for e in t.validate(self.doc,self.root)))
    def test_path_traversal(self):
        self.doc['beats'][0]['audio_path']='../outside.wav'
        self.assertTrue(any('escapes' in e for e in t.validate(self.doc,self.root)))
    def test_symlink_escape(self):
        try: (self.root/'assets'/'escape').symlink_to(self.root.parent,target_is_directory=True)
        except (OSError,NotImplementedError) as e: self.skipTest('cannot create symlink here: '+str(e))
        with self.assertRaises(ValueError): t.inside(self.root,'assets/escape/outside.wav')
    def test_missing_assets_and_final_gates(self):
        errs=t.validate(self.doc,self.root,True,True)
        self.assertTrue(any('Approval' in e for e in errs));self.assertTrue(any('Missing asset' in e for e in errs))
    def test_pilot_lets_pending_claims_through(self):
        self.doc['assets']=[];self.doc['approvals']={'story':'approved','pilot':'approved'}
        for b in self.doc['beats']: b['asset_ids']=[]
        for c in self.doc['claims']: c['status']='pending'
        self.assertTrue(any('Unverified used claim' in e for e in t.validate(self.doc,self.root,False,True)))
        self.assertFalse(any('Unverified used claim' in e for e in t.validate(self.doc,self.root,False,True,True)))
    def test_invalid_motion(self):
        self.doc['beats'][0]['events'][0]['target']='fake'
        self.assertTrue(any('Unknown event' in e for e in t.validate(self.doc,self.root)))

    def test_event_outside_measured_slot_is_rejected(self):
        self.doc['beats'][0]['slot_duration_s'] = 1.0
        self.doc['beats'][0]['events'][0]['time_s'] = 1.0
        self.assertTrue(any('Event outside slot' in e for e in t.validate(self.doc,self.root)))
    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg required')
    def test_measure_assemble_and_stale(self):
        # Tiny test format deliberately not the user's production format.
        self.doc['format']={'width':160,'height':284,'fps':30}
        self.doc['assets']=[]
        for b in self.doc['beats']: b['asset_ids']=[];b['tail_s']=0.1
        self.doc['approvals']={'story':'approved','pilot':'approved'}
        t.save(self.root/'project.json',self.doc)
        for b in self.doc['beats']:
            t.run(['ffmpeg','-v','error','-f','lavfi','-i','sine=frequency=440:sample_rate=48000','-t','0.5',self.root/b['audio_path']])
            t.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=blue:s=160x284:r=30','-t','0.6','-c:v','libx264','-pix_fmt','yuv420p',self.root/b['clip_path']])
        measured=t.measure(self.root)
        self.assertAlmostEqual(measured['total_duration_s'],1.2,places=4)
        # A stale saved duration must be replaced by measured audio.
        measured['beats'][0]['slot_duration_s']=99;t.save(self.root/'project.json',measured)
        self.assertAlmostEqual(t.measure(self.root)['beats'][0]['slot_duration_s'],.6,places=4)
        d=t.load(self.root)
        for c in d['claims']: c['status']='pending'
        t.save(self.root/'project.json',d)
        with self.assertRaisesRegex(ValueError,'Unverified'):t.assemble(self.root)
        manifest=t.assemble(self.root,pilot=True)
        self.assertTrue(manifest['pilot']);self.assertTrue(manifest['unverified_claims'])
        self.assertLess(abs(manifest['measured_duration_s']-1.2),.15)
        self.assertTrue((self.root/'final'/'film.mp4').is_file())
        with self.assertRaises(ValueError):t.assemble(self.root,pilot=True)
        (self.root/'final'/'film.mp4').unlink()
        d=t.load(self.root);d['beats'][0]['narration']+=' Thay lời.';t.save(self.root/'project.json',d)
        with self.assertRaisesRegex(ValueError,'Stale'):t.assemble(self.root,pilot=True)
        with self.assertRaisesRegex(ValueError,'Narration changed'):t.measure(self.root)
    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg required')
    def test_short_clip_rejected(self):
        self.doc['assets']=[];self.doc['approvals']={'story':'approved','pilot':'approved'}
        for b in self.doc['beats']:
            b['asset_ids']=[]
            t.run(['ffmpeg','-v','error','-f','lavfi','-i','sine=frequency=440','-t','0.5',self.root/b['audio_path']])
            t.run(['ffmpeg','-v','error','-f','lavfi','-i','color=s=160x284:r=30','-t','0.2','-c:v','libx264',self.root/b['clip_path']])
        t.save(self.root/'project.json',self.doc);t.measure(self.root)
        with self.assertRaisesRegex(ValueError,'too short'):t.assemble(self.root)

if __name__=='__main__': unittest.main(verbosity=2)
