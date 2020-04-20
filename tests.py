import unittest

from captcha_paint import Line

class PointOnLineTests(unittest.TestCase):

  def test_ok_vertical(self):
    line = Line(0,0,0,10)
    self.assertTrue(line.contains(0, 5))

  def test_ok_horizontal(self):
    line = Line(0, 0, 10, 0)
    self.assertTrue(line.contains(3, 0))

  def test_fail_vertical(self):
    line = Line(0,0,0,10)
    self.assertFalse(line.contains(0, 20))

class LineOverlapTests(unittest.TestCase):
  def test_no_overlap(self):
    line1 = Line(10,10,20,10)
    line2 = Line(0, 0, 0, 10)
    self.assertIsNone(line1.overlap(line2))

  def test_vertical_overlap(self):
    line1 = Line(0, 0, 0, 10)
    line2 = Line(0, 5, 0, 15)
    result = line1.overlap(line2)
    self.assertEqual(result.x1, 0)
    self.assertEqual(result.x2, 0)
    self.assertEqual(result.y1, 5)
    self.assertEqual(result.y2, 10)

  def test_vertical_containment(self):
    line1 = Line(0, 0, 0, 15)
    line2 = Line(0, 5, 0, 10)
    result = line1.overlap(line2)
    self.assertEqual(result.x1, 0)
    self.assertEqual(result.x2, 0)
    self.assertEqual(result.y1, 5)
    self.assertEqual(result.y2, 10)

if __name__ == '__main__':
    unittest.main()