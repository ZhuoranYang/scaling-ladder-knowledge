"""Regression tests for scientific-evidence and retrieval failure modes."""
import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import kb


class KnowledgeContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline=kb.current_data()

    def setUp(self):
        self.pages,self.claims,self.versions,self.questions,self.schema,self.vocabulary,self.aliases=copy.deepcopy(self.baseline)

    def validate(self,verify=False,preserve=False):
        return kb.validate(self.pages,self.claims,self.versions,self.questions,self.schema,self.vocabulary,self.aliases,verify,preserve)

    def wiki(self):
        return next(p for p in self.pages if p['id']=='technique-hyperparameter-transfer')

    def test_current_corpus_has_valid_contracts(self):
        self.assertEqual(self.validate(),[])

    def test_unknown_tag_is_rejected(self):
        self.wiki()['tags'].append('unreviewed-new-tag')
        self.assertTrue(any('unknown tags' in e for e in self.validate()))

    def test_alias_collision_is_rejected(self):
        self.aliases['mup'].append('wd')
        self.assertTrue(any('ambiguous alias' in e for e in self.validate()))

    def test_ignored_source_reference_is_rejected(self):
        self.wiki()['sources'].append('pr-does-not-exist')
        self.assertTrue(any('unresolved sources' in e for e in self.validate()))

    def test_duplicate_page_id_is_rejected(self):
        self.pages.append(copy.deepcopy(self.wiki()))
        self.assertTrue(any('duplicate ID' in e for e in self.validate()))

    def test_confidence_cannot_be_promoted_without_basis(self):
        self.wiki()['confidence']='verified'
        self.assertTrue(any('verified requires' in e for e in self.validate()))

    def test_local_analysis_does_not_masquerade_as_official_or_upstream(self):
        p=self.wiki();p['confidence']='verified';p['sources'].append('doc-local-workbench')
        p['evidence_basis']={'official_sources':['doc-local-workbench'],'upstream_code':['doc-local-workbench']}
        self.assertTrue(any('wrong evidence category' in e for e in self.validate()))

    def test_cpu_receipt_does_not_certify_training_reproduction(self):
        self.claims[0]['verification']={'level':'training_reproduced','receipt':'knowledge/receipts/compute-ledger.json'}
        self.assertTrue(any('no accepted GPU training' in e for e in self.validate()))

    def test_cpu_measurement_must_match_its_receipt(self):
        c=next(c for c in self.claims if c['id']=='claim-marin-hf-records')
        c['verification']['result_checks'][0]['equals']=117
        self.assertTrue(any('receipt result mismatch' in e for e in self.validate()))

    def test_performance_value_is_bound_to_claim(self):
        p=next(p for p in self.pages if p['id']=='case-marin-reproduction')
        p['performance_claims'][0]['value']=.5
        self.assertTrue(any('performance value differs' in e for e in self.validate()))

    def test_pr_merged_status_must_match_captured_record(self):
        p=next(p for p in self.pages if p['id']=='pr-marin-8656')
        p['merged']=True
        self.assertTrue(any('PR card differs from captured' in e for e in self.validate()))

    def test_version_backreferences_cannot_drift(self):
        self.versions[0]['claims']=[]
        self.assertTrue(any('version backreference missing' in e for e in self.validate()))

    def test_page_version_pointers_must_cover_claim_dependencies(self):
        self.wiki()['version_sensitive']=[]
        self.assertTrue(any('missing page version pointer' in e for e in self.validate()))

    def test_prerequisite_cycle_is_rejected(self):
        p=next(p for p in self.pages if p['id']=='governance-evidence-standard')
        p['prerequisites']=['technique-hyperparameter-transfer']
        self.assertTrue(any('prerequisite cycle' in e for e in self.validate()))

    def test_required_question_cannot_be_deleted_to_pass(self):
        self.questions=self.questions[1:]
        self.assertTrue(any('question roster changed' in e for e in self.validate()))

    def test_runnable_scope_cannot_hide_missing_code(self):
        self.wiki()['code_examples']=[]
        self.assertTrue(any('requires actual code examples' in e for e in self.validate()))

    def test_alias_search_reaches_the_canonical_protocol(self):
        for alias in ['mup','muP','μP']:
            result=kb.query_pages(self.pages,tag=alias,kind='technique',aliases=self.aliases)
            self.assertIn('technique-hyperparameter-transfer',[p['id'] for p in result])

    def test_original_paper_removal_is_detected_without_deleting_it(self):
        original=next(e['path'] for e in kb.read_json('knowledge/literature-baseline.json')['files'] if e['path'].endswith('paper.pdf'))
        target=kb.ROOT/original;real_is_file=Path.is_file
        def is_file(path):
            return False if path==target else real_is_file(path)
        with patch.object(Path,'is_file',is_file):
            errors=self.validate(preserve=True)
        self.assertTrue(any('original literature removed: '+original in e for e in errors))
        self.assertTrue(target.is_file())

    def test_pdf_cannot_keep_stale_source_fingerprint(self):
        manifest=kb.read_json('pdf/manifest.json')
        manifest['documents'][0]['source_sha256']='0'*64
        self.assertTrue(any('PDF source is stale' in e for e in kb.validate_pdf_manifest(manifest)))


if __name__=='__main__':unittest.main()
