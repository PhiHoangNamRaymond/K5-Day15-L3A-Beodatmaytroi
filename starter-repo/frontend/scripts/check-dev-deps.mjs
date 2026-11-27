try {
  import.meta.resolve("vite");
  import.meta.resolve("@vitejs/plugin-react");
} catch (error) {
  if (error.code !== "ERR_MODULE_NOT_FOUND") throw error;
  console.error("Thiếu dependency dev. Chạy trong thư mục frontend:");
  console.error("  npm ci --include=dev");
  console.error("  npm run dev");
  process.exitCode = 1;
}
