frappe.listview_settings["pks"] = {
    add_fields: ["status_pks"],
    hide_name_column: true,
    get_indicator: function (doc) {
        if (doc.status_pks == "Tidak Aktif") {
            return [__(doc.status_pks), "red", "status_pks,=," + doc.status_pks];
        } else if (doc.status_pks == "Aktif") {
            return [__(doc.status_pks), "green", "status_pks,=," + doc.status_pks];
        } else if (doc.status_pks == "Masa Tenggang") {
            return [__(doc.status_pks), "orange", "status_pks,=," + doc.status_pks];
        }
    },
    refresh: function (listview) {
        $(".list-row").each(function (e) {
            console.log($(this).find(".indicator-pill .ellipsis").first().text());
            console.log($(this).find(".indicator-pill .ellipsis").first().text().trim() == "Masa Tenggang");
            if ($(this).find(".indicator-pill .ellipsis").first().text().trim() == "Masa Tenggang") {
                $(this).css("background-color", "#e3962bff");
            } else if ($(this).find(".indicator-pill .ellipsis").first().text().trim() == "Tidak Aktif") {
                $(this).css("background-color", "hsla(0, 96%, 65%, 1.00)");
            } else if ($(this).find(".indicator-pill .ellipsis").first().text().trim() == "Aktif") {
                $(this).css("background-color", "#3de94bff");
            }
        });
    },
    before_render: function (doc) {
        frappe.call({
            method: "hrms_custom.hrms_costom.doctype.pks.pks.update_status_list",
            args: {},
            freze: true,
            freze_message: "Updating Status...",
            callback: function (r) {
                if (r.message) {
                    doc.status_pks = r.message;
                    cur_list.refresh();
                }
            },
            error: function (r) {
                console.log(r);
            }
        });
    }
};