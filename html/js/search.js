const project_collection_name = "dig-ed-cat"
const main_search_field = "edition_name"
const search_api_key = "O4BPj7ANU1B5nhTj7rCRrX0Q4GvWrnFb"  // custom search only key

const DEFAULT_CSS_CLASSES = {
    searchableInput: "form-control form-control-sm m-2 border-light-2",
    searchableSubmit: "d-none",
    searchableReset: "d-none",
    showMore: "btn btn-secondary btn-sm align-content-center",
    list: "list-unstyled",
    count: "badge m-2 badge-secondary",
    label: "d-flex align-items-center text-capitalize",
    checkbox: "m-2",
}

const typesenseInstantsearchAdapter = new TypesenseInstantSearchAdapter({
    server: {
        apiKey: search_api_key,
        nodes: [
            {
                host: "typesense.acdh-dev.oeaw.ac.at",
                port: "443",
                protocol: "https",
            },
        ],
    },
    additionalSearchParameters: {
        query_by: main_search_field,
    },
});

const searchClient = typesenseInstantsearchAdapter.searchClient;
const search = instantsearch({
    searchClient,
    indexName: project_collection_name,
    routing: {
        router: instantsearch.routers.history(),
        stateMapping: instantsearch.stateMappings.simple(),
      },
});

search.addWidgets([
    instantsearch.widgets.searchBox({
        container: "#searchbox",
        autofocus: true,
        placeholder: 'Suchen',
        cssClasses: {
            form: "form-inline",
            input: "form-control col-md-11",
            submit: "btn",
            reset: "btn",
        },
    }),

    instantsearch.widgets.hits({
        container: "#hits",
        cssClasses: {
            item: "w-100"
        },
        templates: {
            empty: "Keine Resultate für <q>{{ query }}</q>",
            item(hit, { html, components }) {
                return html` 
            <h3><a href="${hit.resolver}">${hit.edition_name}</a></h3>
            <p>${hit.manager_or_editor.map((item) => html`<span class="badge rounded-pill m-1 bg-success">${item}</span>`)}</p>
            <p>${hit.institution_s.map((item) => html`<a href='${item.resolver}'><span class="badge rounded-pill m-1 bg-danger">${item.institution_name}</span></a>`)}</p>`;
            },
        },
    }),

    instantsearch.widgets.pagination({
        container: "#pagination",
    }),

    instantsearch.widgets.clearRefinements({
        container: "#clear-refinements",
        templates: {
            resetLabel: "Filter zurücksetzen",
        },
        cssClasses: {
            button: "btn",
        },
    }),


    instantsearch.widgets.currentRefinements({
        container: "#current-refinements",
        cssClasses: {
            delete: "btn",
            label: "badge",
        },
    }),

    instantsearch.widgets.stats({
        container: "#stats-container",

    }),

    instantsearch.widgets.panel({
        collapsed: ({ state }) => {
            return state.query.length === 0;
        },
        templates: {
            header: 'Historical Period',
        },
    })(instantsearch.widgets.refinementList)({
        container: "#refinement-list-historical_period",
        attribute: "historical_period",
        searchable: false,
        showMore: false,
        showMoreLimit: 25,
        limit: 10,
        cssClasses: DEFAULT_CSS_CLASSES,
    }),

    instantsearch.widgets.panel({
        collapsed: ({ state }) => {
            return state.query.length === 0;
        },
        templates: {
            header: 'Institutions',
        },
    })(instantsearch.widgets.refinementList)({
        container: "#refinement-list-institution_s",
        attribute: "institution_s.institution_name",
        searchable: true,
        showMore: true,
        showMoreLimit: 50,
        limit: 10,
        searchablePlaceholder: "Search for Institutions",
        cssClasses: DEFAULT_CSS_CLASSES,
    }),

    instantsearch.widgets.panel({
        collapsed: ({ state }) => {
            return state.query.length === 0;
        },
        templates: {
            header: 'Language',
        },
    })(instantsearch.widgets.refinementList)({
        container: "#refinement-list-language",
        attribute: "language",
        searchable: true,
        showMore: true,
        showMoreLimit: 50,
        limit: 10,
        searchablePlaceholder: "Search for Language",
        cssClasses: DEFAULT_CSS_CLASSES,
    }),
    


    instantsearch.widgets.configure({
        hitsPerPage: 10,
        //attributesToSnippet: [main_search_field],
        attributesToSnippet: ["full_text"],
    }),

]);

// Add faceted search widgets dynamically from fields.json
fetch('data/fields.json')
    .then(response => response.json())
    .then(fields => {
        const facetWidgets = fields
            .filter(field => field.facet === true)
            .map(field => 
                instantsearch.widgets.panel({
                    collapsed: ({ state }) => {
                        return state.query.length === 0;
                    },
                    templates: {
                        header: field.verbose_name,
                    },
                })(instantsearch.widgets.refinementList)({
                    container: `#refinement-list-${field.name}`,
                    attribute: field.name,
                    searchable: true,
                    showMore: true,
                    showMoreLimit: 50,
                    limit: 10,
                    searchablePlaceholder: `Search for ${field.verbose_name}`,
                    cssClasses: DEFAULT_CSS_CLASSES,
                })
            );
        
        search.addWidgets(facetWidgets);
    });

search.start();