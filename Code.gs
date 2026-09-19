function doGet(e) {
  const request = {
    file_ID: e.parameter.file_ID,
    named_range: e.parameter.named_range,
    input:
      e.parameter.input !== undefined &&
      e.parameter.input !== null &&
      e.parameter.input !== ""
        ? JSON.parse(e.parameter.input)
        : null
  };

  return runRequest(e, request);
}


function doPost(e) {
  const request = JSON.parse(e.postData.contents);

  return runRequest(e, {
    file_ID: request.file_ID,
    named_range: request.named_range,
    input:
      Object.prototype.hasOwnProperty.call(request, "input")
        ? request.input
        : null
  });
}


function runRequest(e, request) {
  const fileId = request.file_ID;
  const startAddress = request.named_range;
  const initialInput = request.input;

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

  let step = iterator.next(initialInput);

  while (!step.done) {
    step = iterator.next(step.value);
  }

  const resultRange = spreadsheet.getRangeByName("RESULT");

  if (!resultRange) {
    throw new Error("Named range not found: RESULT");
  }

  resultRange.setValue(JSON.stringify(step.value));

  return ContentService
    .createTextOutput("0")
    .setMimeType(ContentService.MimeType.TEXT);
}
