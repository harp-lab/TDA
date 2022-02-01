const CHART_COLORS = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};
$(document).ready(function () {

    function set_subject_options() {
        var subjects = "";
        for (var i = 1; i <= 316; i++) {
            subjects += "<option value='" + i + "'>Subject " + i + "</option>";
        }
        $("#subject_id").html(subjects);
    }

    set_subject_options();
    $("#graph").hide();

    function get_json_data(data_path) {
        var rows = [];
        $.ajax({
            url: data_path,
            type: "GET",
            async: false,
            dataType: "json",
            success: function (data) {
                rows = data;
            },
        });
        return $.parseJSON(rows);
    }


    function show_graph(rows, chart_title) {
        const canvas_background_plugin = {
            id: 'custom_canvas_background_color',
            beforeDraw: (chart) => {
                const ctx = chart.canvas.getContext('2d');
                ctx.save();
                ctx.globalCompositeOperation = 'destination-over';
                ctx.fillStyle = 'white';
                ctx.fillRect(0, 0, chart.width, chart.height);
                ctx.restore();
            }
        };

        var chart_data = [];
        for (var i = 0; i < rows.length; i++) {
            chart_data.push({
                x: parseFloat(rows[i][0]),
                y: parseFloat(rows[i][1])
            });
        }
        const config = {
            type: 'scatter',
            data: {
                datasets: [
                    {
                        label: 'Timeslots',
                        data: chart_data,
                        borderColor: CHART_COLORS.green,
                        backgroundColor: CHART_COLORS.green,
                        pointStyle: 'circle',
                        pointRadius: 4,
                        hoverRadius: 4

                    }],
            },
            options: {
                animation: false,
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            align: 'center',
                            text: 'MDS 1'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            align: 'center',
                            text: 'MDS 2'
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: chart_title,
                        padding: {
                            top: 10,
                            bottom: 10
                        },
                        font: {
                            size: 18
                        }
                    },
                    canvas_background_plugin,
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                let label = "Timeslot " + context.dataIndex;
                                return label;
                            }
                        }
                    }
                }
            },
        };
        Chart.defaults.color = '#000';
        const ctx = document.getElementById('visualization_div').getContext('2d');

        const old_chart = Chart.getChart(ctx);
        if (typeof old_chart !== 'undefined') {
            old_chart.destroy();
        }
        new Chart(ctx, config);
    }

    $(".download_chart").on("click", function () {
        const id = $(this).attr("id");
        let canvas_data, filename;
        const ctx = document.getElementById('visualization_div').getContext('2d');
        const current_chart = Chart.getChart(ctx);
        if (typeof current_chart !== 'undefined') {
            if (id === "jpeg_btn") {
                canvas_data = current_chart.toBase64Image('image/jpeg', 1);
                filename = "matrix_graph.jpg";
            } else if (id === "png_btn") {
                canvas_data = current_chart.toBase64Image();
                filename = "matrix_graph.png";
            } else if (id === "pdf_btn") {
                const aspect_ratio = current_chart.width / current_chart.height;
                filename = "matrix_graph.pdf";
                var pdf = new jsPDF('l', 'pt', 'a4');
                const pdf_width = pdf.internal.pageSize.width;
                const pdf_width_px = get_pdf_size(pdf_width, 'px');
                if (current_chart.width > pdf_width_px) {
                    current_chart.resize(pdf_width, pdf_width * (1.0 / aspect_ratio));
                }
                canvas_data = current_chart.toBase64Image();
                pdf.addImage(canvas_data, 'PNG', 0, 20);
                pdf.save(filename);
                current_chart.resize();
            }
        }
        if (id !== "pdf_btn") {
            let temp_link = document.createElement('a');
            temp_link.href = canvas_data;
            temp_link.download = filename;
            temp_link.click();
        }
    });
    $(".graph_data_btn").on("click", function () {
        var subject_id = $('#subject_id')[0].value;
        var data_path = 'subjects_mds/subject_' + subject_id + '.json';
        var data = get_json_data(data_path);
        $("#graph").hide();
        show_graph(data, "MDS for Subject " + subject_id);
        $("#graph").show("slow");
    });

});