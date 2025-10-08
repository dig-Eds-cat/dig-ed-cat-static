function linkToDetailView(cell) {
  var row = cell.getRow().getData();
  return `<a href="${row.resolver}">${row.edition_name}</a>`;
}

const linkListColumnSettings = {
  formatter: linkListFormatter,
  headerFilter: "input",
  headerFilterFunc: customHeaderFilter,
  sorter: "array",
};

function customHeaderFilter(headerValue, rowValue, rowData, filterParams) {
  // for columns where the name of the items is not in the "value" field,
  // the line headerFilterFuncParams: { nameField: 'name' } needs to be added to the column config
  if (filterParams.nameField) {
    return rowValue.some(function (item) {
      return item[filterParams.nameField]
        .toLowerCase()
        .includes(headerValue.toLowerCase());
    });
  } else {
    return rowValue.some(function (item) {
      return item.value.toLowerCase().includes(headerValue.toLowerCase());
    });
  }
}

function linkListFormatter(cell, formatterParams, onRendered) {
  let value = cell.getValue();
  let output = value
    .map((item) => {
      return `<li><a href="${formatterParams.urlPrefix}${
        item[formatterParams.idField]
      }">${item[formatterParams.nameField]}</a></li>`;
    })
    .join(" ");
  output = `<ul>${output}</ul>`;
  let renderer = this;
  if (formatterParams.scrollable === true) {
    output = get_scrollable_cell(renderer, cell, output);
  }
  return output;
}

var table = new Tabulator("#example-table", {
  ajaxURL: "data/editions.json",
  height: "800",
  width: "800",
  layout: "fitColumns",
  responsiveLayout: "collapse",
  columns: [
    { title: "ID", field: "id", width: 80, headerFilter: "input" },
    {
      title: "Name",
      field: "edition_name",
      minWidth: 300,
      headerFilter: "input",
      formatter: linkToDetailView,
    },
    {
      title: "Historical Period",
      field: "historical_period",
      headerFilter: "input",
    },
    {
      title: "Institutions",
      field: "institution_s",
      ...linkListColumnSettings,
      formatterParams: {
        urlPrefix: "",
        idField: "resolver",
        nameField: "institution_name",
      },
      headerFilterFuncParams: { nameField: "institution_name" },
    },
    { title: "Language", field: "language", headerFilter: "input", width: 150 },
    { title: "URL", field: "url", formatter: "link", headerFilter: "input" },
    { title: "Alive", field: "current_availability", headerFilter: "input" },
  ],
});

table.on("dataLoaded", function (data) {
  var el = document.getElementById("counter1");
  el.innerHTML = `${data.length}`;
  var el = document.getElementById("counter2");
  el.innerHTML = `${data.length}`;
});

table.on("dataFiltered", function (filters, data) {
  var el = document.getElementById("counter1");
  el.innerHTML = `${data.length}`;
});

document.getElementById("download-csv").addEventListener("click", function () {
  table.download("csv", "dig-ed-cat.csv");
});

document.getElementById("download-excel").addEventListener("click", function () {
  table.download("xlsx", "dig-ed-cat.xlsx", {sheetName:"digedcat"}); 
});
document.getElementById("download-json").addEventListener("click", function () {
  table.download("json", "dig-ed-cat.json"); 
});
