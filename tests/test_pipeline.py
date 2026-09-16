import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from pipeline import load, validate

class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.c,cls.m,cls.p,cls.s=load()
    def test_all_validation_rules(self): self.assertTrue(all(validate(self.c,self.m,self.p,self.s).values()))
    def test_exact_claim_count(self): self.assertEqual(len(self.c),50000)
    def test_unique_claim_ids(self): self.assertTrue(self.c.claim_id.is_unique)
    def test_foreign_keys(self):
        self.assertTrue(self.c.member_id.isin(self.m.member_id).all())
        self.assertTrue(self.c.provider_id.isin(self.p.provider_id).all())
        self.assertTrue(self.c.service_code.isin(self.s.service_code).all())
    def test_financial_reconciliation(self):
        paid=self.c.claim_status.eq("Paid")
        self.assertTrue(((self.c.loc[paid,"paid_amount"]+self.c.loc[paid,"member_cost_share"]-self.c.loc[paid,"allowed_amount"]).abs()<=.01).all())

if __name__=="__main__": unittest.main()

