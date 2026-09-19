function doGet(e) {
  const fileId = e.parameter.file_ID;
  const startAddress = e.parameter.named_range;

  if (!fileId || !startAddress) {
    return ContentService
      .createTextOutput("0")
      .setMimeType(ContentService.MimeType.TEXT);
  }

  const spreadsheet = SpreadsheetApp.openById(fileId);
  let address = startAddress;

  const iterator = {
    next: function (input) {
      if (address === null) {
        return {
          done: true,
          value: input
        };
      }

      const currentAddress = address;
      const range = spreadsheet.getRangeByName(currentAddress);

      if (!range) {
        throw new Error("Named range not found: " + currentAddress);
      }

      const source = range.getValue();

      if (typeof source !== "string" || source.trim() === "") {
        throw new Error("No executable function at named range: " + currentAddress);
      }

      const fn = eval("(" + source + ")");

      if (typeof fn !== "function") {
        throw new Error("Named range did not resolve to a function: " + currentAddress);
      }

      const output = fn({
        event: e,
        spreadsheet: spreadsheet,
        input: input,
        address: currentAddress
      });

      const hasNextAddress =
        output !== null &&
        typeof output === "object" &&
        Object.prototype.hasOwnProperty.call(output, "next_address");

      address = hasNextAddress && output.next_address !== ""
        ? output.next_address
        : null;

      return {
        done: address === null,
        value: output
      };
    }
  };

  let step = iterator.next(null);

  while (!step.done) {
    step = iterator.next(step.value);
  }

  return ContentService
    .createTextOutput("0")
    .setMimeType(ContentService.MimeType.TEXT);
}
