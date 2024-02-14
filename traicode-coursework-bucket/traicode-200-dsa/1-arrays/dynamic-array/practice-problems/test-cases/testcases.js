// const adjustIndentation = (str) => {
//     const lines = str.split("\n");
//     const newlines = lines.map((line) => line.trim()).join("\n") + "\n";

//     return newlines;
// }

const testCases = [
  {
    testName: "test_resize_1",
    input: ["DynamicArray", [], "resize", 10, "resize", 5],
    expectedOutput: "[10, 5]",
  },
  {
    testName: "test_append_1",
    input: ["DynamicArray", [], "append", 1, "append", 2],
    expectedOutput: "[1, 2]",
  },
  {
    testName: "test_insert_at_index_1",
    input: ["DynamicArray", [1, 2, 3], "insert_at_index", 0, 0],
    expectedOutput: "[0, 1, 2, 3]",
  },
  {
    testName: "test_insert_at_index_2",
    input: ["DynamicArray", [0, 1, 2, 3], "insert_at_index", 2, 1.5, "insert_at_index", 5, 4],
    expectedOutput: "[0, 1, 1.5, 2, 3, 4]",
  },
  {
    testName: "test_remove_at_index_1",
    input: ["DynamicArray", [1, 2, 3, 4, 5], "remove_at_index", 2],
    expectedOutput: "[1, 2, 4, 5]",
  }
]

// const testingDB = {
//   "resize": [
//     {
//       input: ["DynamicArray", [], "resize", 10, "resize", 5],
//       expectedOutput: "[10, 5]",
//     }],
//   "append": [
//     {
//       input: ["DynamicArray", [], "append", 1, "append", 2],
//       expectedOutput: "[1, 2]",
//     }],
//   "insert_at_index": [
//     {
//       input: ["DynamicArray", [1, 2, 3], "insert_at_index", 0, 0],
//       expectedOutput: "[0, 1, 2, 3]",
//     },
//     {
//       input: ["DynamicArray", [0, 1, 2, 3], "insert_at_index", 2, 1.5, "insert_at_index", 5, 4],
//       expectedOutput: "[0, 1, 1.5, 2, 3, 4]",
//     }]
// };

const fs = require("fs");

// Convert object to JSON string
const jsonData = JSON.stringify(testCases, null, 2); // 2 is for indentation (optional)

// Write JSON string to a file
fs.writeFile("data.json", jsonData, (err) => {
  if (err) {
    console.error("Error writing JSON file:", err);
  } else {
    console.log("JSON file has been saved successfully.");
  }
});
