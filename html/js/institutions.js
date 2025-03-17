function linkToDetailView(cell) {
    var row = cell.getRow().getData()
    return `<a href="${row.resolver}">${row.institution_name}</a>`
}

const linkListColumnSettings = {
    formatter: linkListFormatter,
    headerFilter: 'input',
    headerFilterFunc: customHeaderFilter,
    sorter: 'array'
}

function customHeaderFilter(headerValue, rowValue, rowData, filterParams) {
    // for columns where the name of the items is not in the "value" field,
    // the line headerFilterFuncParams: { nameField: 'name' } needs to be added to the column config
    if (filterParams.nameField) {
        return rowValue.some(function (item) {
            return item[filterParams.nameField]
                .toLowerCase()
                .includes(headerValue.toLowerCase())
        })
    } else {
        return rowValue.some(function (item) {
            return item.value.toLowerCase().includes(headerValue.toLowerCase())
        })
    }
}

function linkListFormatter(cell, formatterParams, onRendered) {
    let value = cell.getValue()
    let output = value
        .map(item => {
            return `<li><a href="${formatterParams.urlPrefix}${item[formatterParams.idField]
                }.html">${item[formatterParams.nameField]}</a></li>`
        })
        .join(' ')
    output = `<ul>${output}</ul>`
    let renderer = this
    if (formatterParams.scrollable === true) {
        output = get_scrollable_cell(renderer, cell, output)
    }
    return output
}

var table = new Tabulator("#example-table", {
    ajaxURL: "data/institutions.json",
    height: "800",
    width: "800",
    layout: "fitColumns",
    responsiveLayout: "collapse",
    columns: [
        { title: "ID", field: "id", width: 80, headerFilter: "input" },
        { title: "Name", field: "institution_name", minWidth: 300, headerFilter: "input", formatter: linkToDetailView },
        { title: "Country", field: "part_of", headerFilter: "input" },
        { title: "Editions", field: "edition_counter", headerFilter: "input" },
    ]
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
