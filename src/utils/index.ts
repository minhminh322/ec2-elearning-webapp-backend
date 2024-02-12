type Language =
  | "javascript"
  | "typescript"
  | "python"
  | "java"
  | "c#"
  | "c"
  | "unknown";

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
