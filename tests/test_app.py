import unittest,app
class SitemapTests(unittest.TestCase):
 def test_duplicate(self):
  x=b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://a.test/</loc></url><url><loc>https://a.test/</loc><lastmod>not-a-date</lastmod></url></urlset>'
  r=app.validate(x)
  self.assertEqual(r["count"],2)
  self.assertTrue(any("duplicate" in i["message"] for i in r["issues"]))
if __name__=="__main__":unittest.main()
