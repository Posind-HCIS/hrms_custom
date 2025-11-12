// public/js/dump_doc/list.js
// Customize dump_doc list view

frappe.listview_settings['dump_doc'] = {
    // Fetch field biar data available client-side
    add_fields: ["nama", "option", "gas", "modified"],

    // Pakai onload buat modifikasi kolom (ini cara standard)
    onload: function(listview) {
        // Override atau tambah kolom (array of objects)
        listview.columns = [
            {
                fieldname: "name",  // Kolom default ID
                label: "ID",
                width: 100
            },
            {
                fieldname: "nama",  // Bener, pakai fieldname
                label: "Nama",
                width: 150
            },
            {
                fieldname: "option",
                label: "Option",
                width: 100
            },
            {
                fieldname: "gas",
                label: "Gas?",
                width: 80,
                formatter: function(value, row, column, data) {
                    if (value) {
                        return '<span style="color: green; font-weight: bold;">✓ Ya</span>';
                    } else {
                        return '<span style="color: red;">✗ Tidak</span>';
                    }
                }
            },
            {
                fieldname: "modified",
                label: "Modified",
                width: 120
            }
        ];

        // Force rebuild header & render data
        setTimeout(() => {
            listview.render_header();
            listview.render();
        }, 100);  // Delay kecil biar data ke-load dulu
    },

    // Optional: Rebuild tiap refresh list
    refresh: function(listview) {
        setTimeout(() => {
            listview.render_header();
            listview.render();
        }, 100);
    }
};

console.log('✓ dump_doc list view customization applied');