import unittest
import importlib

# Import the module
sm = importlib.import_module("student_mgmt")

class TestStudentMgmt(unittest.TestCase):
    def setUp(self):
        # Reset in-memory data
        sm.students.clear()

    def test_add_and_search(self):
        sm.students.append({"roll_no": "101", "name": "Alice", "grade": "A", "age": "15"})
        found = sm.search_by_roll("101")
        self.assertIsNotNone(found)
        self.assertEqual(found["name"], "Alice")

    def test_duplicate_roll(self):
        sm.students.append({"roll_no": "101", "name": "Alice", "grade": "A", "age": "15"})
        self.assertIsNotNone(sm.search_by_roll("101"))
        self.assertTrue(any(s["roll_no"] == "101" for s in sm.students))

    def test_update(self):
        sm.students.append({"roll_no": "102", "name": "Bob", "grade": "B", "age": "16"})
        s = sm.search_by_roll("102")
        s["name"] = "Bobby"
        self.assertEqual(sm.search_by_roll("102")["name"], "Bobby")

    def test_delete(self):
        sm.students.append({"roll_no": "103", "name": "Cara", "grade": "A", "age": "17"})
        s = sm.search_by_roll("103")
        sm.students.remove(s)
        self.assertIsNone(sm.search_by_roll("103"))

if __name__ == "__main__":
    unittest.main()
