const testCases = [
  {
    testName: "test_put_example_1",
    input: ["HashTable", [], "put", "key1", "value1"],
    expectedOutput: '["key1", "value1"]',
  },
  {
    testName: "test_put_example_2",
    input: ["HashTable", ["key1", "value1"], "put", "key2", "value2"],
    expectedOutput: '["key1", "value1", "key2", "value2"]',
  },
  {
    testName: "test_resize_example_1",
    input: ["HashTable", [], "resize", 10, "resize", 5],
    expectedOutput: "[10, 5]",
  },
  {
    testName: "test_resize_example_2",
    input: ["HashTable", [], "resize", 5, "resize", 10],
    expectedOutput: "[5, 10]",
  },
  {
    testName: "test_table_load_example_1",
    input: ["HashTable", [], "table_load"],
    expectedOutput: "0",
  },
  {
    testName: "test_table_load_example_2",
    input: ["HashTable", ["key1", "value1", "key2", "value2"], "table_load"],
    expectedOutput: "0.5",
  },
  {
    testName: "test_empty_buckets_example_1",
    input: ["HashTable", [], "empty_buckets"],
    expectedOutput: "0",
  },
  {
    testName: "test_empty_buckets_example_2",
    input: ["HashTable", ["key1", "value1", "key2", "value2"], "empty_buckets"],
    expectedOutput: "0.5",
  },
  {
    testName: "test_get_example_1",
    input: ["HashTable", ["key1", "value1", "key2", "value2"], "get", "key1"],
    expectedOutput: '"value1"',
  },
  {
    testName: "test_get_example_2",
    input: ["HashTable", ["key1", "value1", "key2", "value2"], "get", "key3"],
    expectedOutput: "null",
  },
  {
    testName: "test_contains_key_example_1",
    input: [
      "HashTable",
      ["key1", "value1", "key2", "value2"],
      "contains_key",
      "key1",
    ],
    expectedOutput: "true",
  },
  {
    testName: "test_contains_key_example_2",
    input: [
      "HashTable",
      ["key1", "value1", "key2", "value2"],
      "contains_key",
      "key3",
    ],
    expectedOutput: "false",
  },
  {
    testName: "test_remove_example_1",
    input: [
      "HashTable",
      ["key1", "value1", "key2", "value2"],
      "remove",
      "key1",
    ],
    expectedOutput: '["key2", "value2"]',
  },
  {
    testName: "test_get_keys_and_values_example_1",
    input: [
      "HashTable",
      ["key1", "value1", "key2", "value2"],
      "get_keys_and_values",
    ],
    expectedOutput: '[["key1", "value1"], ["key2", "value2"]]',
  },
  {
    testName: "test_clear_example_1",
    input: ["HashTable", ["key1", "value1", "key2", "value2"], "clear"],
    expectedOutput: "[]",
  },
  {
    testName: "test_clear_example_2",
    input: ["HashTable", [], "clear"],
    expectedOutput: "[]",
  },
];

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
