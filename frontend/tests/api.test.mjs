import test from "node:test";
import assert from "node:assert/strict";
import { api } from "../src/api.js";

const originalFetch = globalThis.fetch;

test("api() - 8 tình huống HTTP giả lập", async (t) => {
  t.afterEach(() => {
    globalThis.fetch = originalFetch;
  });

  await t.test("1. GET thành công đọc và trả về JSON", async () => {
    globalThis.fetch = async () => ({
      status: 200,
      ok: true,
      text: async () => JSON.stringify([{ class_id: "WEB-01" }]),
    });
    const result = await api("/sections");
    assert.deepEqual(result, [{ class_id: "WEB-01" }]);
  });

  await t.test("2. POST gửi body dưới dạng chuỗi JSON và header Content-Type", async () => {
    let capturedOptions;
    globalThis.fetch = async (_url, options) => {
      capturedOptions = options;
      return {
        status: 201,
        ok: true,
        text: async () => JSON.stringify({ message: "Dang ky thanh cong" }),
      };
    };
    const body = { student_id: "22000004", class_section_id: "WEB-01" };
    const result = await api("/enrollments", { method: "POST", body });
    assert.equal(capturedOptions.method, "POST");
    assert.equal(capturedOptions.headers["Content-Type"], "application/json");
    assert.equal(capturedOptions.body, JSON.stringify(body));
    assert.deepEqual(result, { message: "Dang ky thanh cong" });
  });

  await t.test("3. DELETE trả về 204 No Content và hàm trả về null", async () => {
    globalThis.fetch = async () => ({
      status: 204,
      ok: true,
    });
    const result = await api("/enrollments/22000004/WEB-01", { method: "DELETE" });
    assert.equal(result, null);
  });

  await t.test("4. Phản hồi không phải JSON ném lỗi", async () => {
    globalThis.fetch = async () => ({
      status: 200,
      ok: true,
      text: async () => "<html>Internal Server Error</html>",
    });
    await assert.rejects(
      () => api("/test"),
      /HTTP 200: phản hồi không phải JSON\./,
    );
  });

  await t.test("5. Lỗi HTTP với detail dạng chuỗi", async () => {
    globalThis.fetch = async () => ({
      status: 404,
      ok: false,
      text: async () => JSON.stringify({ detail: "Khong tim thay sinh vien" }),
    });
    await assert.rejects(
      () => api("/students/99999999/enrollments"),
      (err) => {
        assert.equal(err.status, 404);
        assert.match(err.message, /HTTP 404: Khong tim thay sinh vien/);
        return true;
      },
    );
  });

  await t.test("6. Lỗi HTTP 422 với detail dạng mảng (validation error)", async () => {
    globalThis.fetch = async () => ({
      status: 422,
      ok: false,
      text: async () => JSON.stringify({
        detail: [
          { loc: ["body", "student_id"], msg: "field required" },
          { loc: ["body", "class_section_id"], msg: "field required" },
        ],
      }),
    });
    await assert.rejects(
      () => api("/enrollments", { method: "POST", body: {} }),
      (err) => {
        assert.equal(err.status, 422);
        assert.match(err.message, /field required; field required/);
        return true;
      },
    );
  });

  await t.test("7. Lỗi mất kết nối mạng ném lỗi kết nối/CORS", async () => {
    globalThis.fetch = async () => {
      throw new TypeError("Failed to fetch");
    };
    await assert.rejects(
      () => api("/sections"),
      /Không nhận được phản hồi API\. Kiểm tra Backend\/CORS/,
    );
  });

  await t.test("8. Bỏ qua và ném tiếp AbortError khi bị hủy", async () => {
    globalThis.fetch = async () => {
      const abortError = new Error("The operation was aborted");
      abortError.name = "AbortError";
      throw abortError;
    };
    await assert.rejects(
      () => api("/sections"),
      (err) => err.name === "AbortError",
    );
  });
});
