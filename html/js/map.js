try {
    const response = await fetch("data/institutions.json");
    const data = await response.json();
    window.__MY_DATA = data;
} catch (error) {
    console.error(error);
}
const data = window.__MY_DATA

console.log(data)
const map = L.map('map').setView([0, 0], 3);
const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
var markers = L.markerClusterGroup();

data.forEach(element => {
    var lat = Number(element.institution_lat);
    var lng = Number(element.institution_lng);
    var label = element.institution_name
    const editionsList = element.editions.map(item => `<li><a href="${item.edition_resolver}">${item.edition_name}</a></li>`).join('');
    var popUp = `<h5 class="text-center">${label}</h5>
    <h6><a href="${element.institution_website}">${element.institution_website}</a></h6>
    <ul>${editionsList}</ul>`
    if (lat) {
        var marker = L.marker([lat, lng], { alt: label }).bindPopup(popUp);
        markers.addLayer(marker);
    }

});
map.addLayer(markers);
map.fitBounds(markers.getBounds())
