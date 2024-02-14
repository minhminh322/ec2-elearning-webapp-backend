import fs from "fs";
import path from "path";

type Language =
  | "javascript"
  | "typescript"
  | "python"
  | "java"
  | "c#"
  | "c"
  | "unknown";

export function readFileAsync(filePath: string) {
  return new Promise((resolve, reject) => {
    fs.readFile(filePath, "utf8", (err, data) => {
      if (err) {
        reject(err);
        return;
      }
      resolve(data);
    });
  });
}

export function getAllFiles(
  dirPath: string,
  filesArr: string[] = []
): string[] {
  const files = fs.readdirSync(dirPath);

  files.forEach((file) => {
    const filePath = path.join(dirPath, file);
    if (fs.statSync(filePath).isDirectory()) {
      // If it's a directory, recursively call getAllFiles
      getAllFiles(filePath, filesArr);
    } else {
      // If it's a file, push its path to filesArr
      filesArr.push(filePath);
    }
  });

  return filesArr;
}

export function detectLanguage(filename: string): Language {
  const extension = filename.split(".").pop();

  switch (extension) {
    case "js":
      return "javascript";
    case "ts":
      return "typescript";
    case "py":
      return "python";
    case "java":
      return "java";
    case "cs":
      return "c#";
    case "c":
      return "c";
    default:
      return "unknown";
  }
}
