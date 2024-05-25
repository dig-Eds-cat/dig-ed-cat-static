function linkToDetailView(cell) {
    var row = cell.getRow().getData()
    var cellData = cell.getData()
    var linkText = row.edition_name
    var theLink = `<a href="${row.resolver}">${linkText}</a>`
    // for locations, the id is in the properties (geoJSON)
    return theLink
}


var table = new Tabulator("#example-table", {
    ajaxURL: "editions.json", //ajax URL
    height: "800",
    layout: "fitColumns",
    responsiveLayout: "collapse",
    pagination: "local",       //paginate the data
    paginationSize: 20,         //allow 25 rows per page of data
    paginationCounter: "rows",
    columns: [ //Define Table Columns
        { title: "Name", field: "edition_name", minWidth: 400, headerFilter: "input", formatter: linkToDetailView },
        { title: "URL", field: "url", formatter: "link", headerFilter: "input" }
    ]
});