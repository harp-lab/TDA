var bar_color = "#001E62";
var bar_hover_color = "#D50032";
var bar_click_color = "#FFBF3F";

function filter_default_mode_network(matrix) {
    // Default mode network's row and column ranges to keep
    const node_ranges = [[43, 54], [100, 111]];
    let new_matrix = [];
    for (let range_i = 0; range_i < node_ranges.length; range_i++) {
        for (let row = node_ranges[range_i][0]; row <= node_ranges[range_i][1]; row++) {
            let temp_row = [];
            for (let range_j = 0; range_j < node_ranges.length; range_j++) {
                for (let column = node_ranges[range_j][0]; column <= node_ranges[range_j][1]; column++) {
                    temp_row.push(matrix[row][column]);
                }
            }
            new_matrix.push(temp_row);
        }
    }
    return new_matrix;

}

async function get_static_data(file_path) {
    let data_file = "data/fmri_data/normalize_dfc_2500_subject_1_time_1.txt";
    // data_file = "../data/demo_data.txt";
    // data_file = "../data/time_varying_4_4.csv";
    if (file_path !== "") {
        data_file = file_path;
    }
    return d3.text(data_file).then(function (text) {
        let matrix;
        if (data_file.endsWith("csv")) {
            matrix = d3.csvParseRows(text, (row) => row.map((value) => +value));
        } else {
            matrix = d3.tsvParseRows(text, (row) => row.map((value) => +value));
        }
        if (matrix) {
            if (matrix.length == 113 && matrix[0].length == 113) {
                return filter_default_mode_network(matrix);
            }
        }
        return matrix;
    });
}


function show_barcode(barcodes, matrix, id_number) {
    $("#barcodes_" + id_number).empty();
    // Select the container with id "barcodes"
    const barcodes_container = d3.select("#barcodes_" + id_number);
    // Remove existing SVG content
    barcodes_container.selectAll("svg").remove();
    // Declare the chart dimensions and margins.
    const margin_top = 20;
    const margin_right = 5;
    const margin_bottom = 5;
    const margin_left = 5;
    const width = barcodes_container.node().getBoundingClientRect().width - 20;
    const bar_height = 10; // Fixed height for the bars

    // Calculate the height of the SVG container based on the number of bars
    const height = barcodes.length * (bar_height + 5) + margin_top + margin_bottom;
    const padding = 5;

    const barcodes_svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height);
    // Sort data by the length of the ranges (largest to smallest)
    barcodes.sort((a, b) => (b[1] - b[0]) - (a[1] - a[0]));
    // Calculate the maximum value in the matrix
    const maxValue = matrix.reduce((max, row) => Math.max(max, ...row), Number.NEGATIVE_INFINITY);


    // Create scales for x and y axes
    const xScale = d3.scaleLinear()
        .domain([0, maxValue])
        .range([0, width]);

    const yScale = d3.scaleBand()
        .domain(d3.range(barcodes.length))
        .range([margin_top + padding, height - margin_bottom])
        .padding(0.1);

    // Create horizontal bars
    barcodes_svg.selectAll("rect")
        .data(barcodes)
        .enter().append("rect")
        .attr("x", d => xScale(d[0]))  // Use d[0] as the starting point
        .attr("y", (d, i) => yScale(i))
        .attr("width", d => xScale(d[1] - d[0]))  // Adjust the width based on the range
        .attr("height", bar_height)
        .attr("fill", bar_color)
        .attr("clicked", "false")
        .attr("class", "bar")
        .on("mouseover", function (event, d) {
            const current_element = d3.select(this);
            if (current_element.attr("clicked") === "false") {
                current_element.attr("fill", bar_hover_color);
            }
            const bar_start = d3.format(".5f")(d[0]);
            const bar_end = d3.format(".5f")(d[1]);

            const msg = `[${bar_start}, ${bar_end})`;
            current_element.style("cursor", "pointer");
            $(this).tooltip({
                title: msg,
                placement: "top",
                trigger: "manual"
            }).tooltip("show");
        })
        .on("mouseout", function (d) {
            const current_element = d3.select(this);
            if (current_element.attr("clicked") === "false") {
                current_element.transition()
                    .duration(200)
                    .attr("fill", bar_color)
            }
            current_element.style("cursor", "auto");
            // Use Bootstrap's tooltip hide with a delay
            const tooltip_element = $(this);
            setTimeout(function () {
                tooltip_element.tooltip("hide");
            }, 100);
        })
        .on("click", function (event, d) {
            const current_element = d3.select(this);
            $("#fcn_" + id_number).empty();
            $("#fcn_graph_start_" + id_number).empty();
            $("#fcn_graph_end_" + id_number).empty();
            if (current_element.attr("clicked") === "false") {
                $("#barcodes_" + id_number + " svg .bar").attr("fill", bar_color);
                $("#barcodes_" + id_number + " svg .bar").attr("clicked", "false");
                current_element.attr("fill", bar_click_color);
                current_element.attr("clicked", "true");
                const msg = `Selected barcode: [${d[0]}, ${d[1]})`;
                $("#fcn_" + id_number).text(msg);
                show_fcn(matrix, d[0], "fcn_graph_start_" + id_number, id_number);
                show_fcn(matrix, d[1], "fcn_graph_end_" + id_number, id_number);
                show_slider(matrix, d[0], d[1], id_number);
            } else {
                current_element.attr("fill", bar_color);
                current_element.attr("clicked", "false");
                show_fcn(matrix, 0, "fcn_graph_start_" + id_number, id_number);
                show_fcn(matrix, 0, "fcn_graph_end_" + id_number, id_number);
                show_slider(matrix, d[0], d[1], id_number);
            }
        });


    const zoom = d3.zoom()
        .scaleExtent([1, 50])
        .on("zoom", zoomed);

    const drag = d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);

    barcodes_svg.call(zoom)
        .call(drag);


    function zoomed(event) {
        const new_xScale = event.transform.rescaleX(xScale);
        barcodes_svg.selectAll("rect")
            .attr("x", d => new_xScale(d[0]))
            .attr("width", d => new_xScale(d[1]) - new_xScale(d[0]));

        barcodes_svg.select(".x-axis")
            .call(xAxis.scale(new_xScale));
    }

    function dragstarted(event) {
        d3.select(this).raise().attr("stroke", "black");
    }

    function dragged(event, d) {
        d3.select(this).attr("y", event.y);
    }

    function dragended(event) {
        d3.select(this).attr("stroke", null);
    }


    const xAxis = d3.axisTop(xScale);

    barcodes_svg.append("g")
        .attr("class", "x-axis") // Add a class for easy selection
        .attr("transform", `translate(0, ${margin_top})`)
        .call(xAxis);

    // Append the SVG element to the container
    barcodes_container.node().append(barcodes_svg.node());

}

function show_slider(matrix, start_value = 0, end_value = 0, id_number) {
    // Flatten the matrix
    let flattened_values = matrix.flat();

    // Get unique values using Set
    let values = [...new Set(flattened_values)].sort();

    $("#slider-container_" + id_number).empty();
    // Select the container with id "barcodes"
    const slider_container = d3.select("#slider-container_" + id_number);
    // Remove existing SVG content
    slider_container.selectAll("svg").remove();
    // Width and height
    const w = slider_container.node().getBoundingClientRect().width - 30;
    const h = 40;
    const min_value = d3.min(values);
    const max_value = d3.max(values);
    if (start_value === 0 && end_value === 0) {
        const msg = `Selected range: [0, 0)`;
        $("#fcn_" + id_number).text(msg);
    }

    // Create SVG element
    const slider_svg = d3.create("svg")
        .attr("width", w)
        .attr("height", h);

    // Create scale for slider
    const x_scale = d3.scaleLinear()
        .domain([min_value, max_value])
        .range([30, w - 30])
        .clamp(true);
    // Radius
    const bar_width = 6;
    const bar_height = 14;

    // Get scaled radius on x axis
    const scaled_bar = (values[1] - values[0]) / (x_scale(values[1]) - x_scale(values[0])) * bar_width;

    const x_axis = d3.axisBottom(x_scale);

    slider_svg.append("g")
        .attr("transform", "translate(0," + h / 2 + ")")
        .call(x_axis);

    // Start bar
    const start_bar = slider_svg.append("rect")
        .attr("x", x_scale(start_value))
        .attr("y", h / 2 - bar_height / 2)
        .attr("width", bar_width * 2)
        .attr("height", bar_height)
        .attr("fill", bar_color)
        .style("cursor", "pointer")
        .call(d3.drag()
            .on("drag", dragged_start_bar));

    // End bar
    const end_bar = slider_svg.append("rect")
        .attr("x", x_scale(end_value))
        .attr("y", h / 2 - bar_height / 2)
        .attr("width", bar_width * 2)
        .attr("height", bar_height)
        .attr("fill", bar_hover_color)
        .style("cursor", "pointer")
        .call(d3.drag()
            .on("drag", dragged_end_bar));


    start_bar.attr("x", x_scale(start_value));

    end_bar.attr("x", x_scale(end_value));


    const filled_color = bar_click_color;
    let filled_width = Math.max(0, parseFloat(end_bar.attr("x")) - parseFloat(start_bar.attr("x")) - (bar_width * 2));

    // Filled area between start_bar and end_bar
    const filled_area = slider_svg.append("rect")
        .attr("x", parseFloat(start_bar.attr("x")) + (bar_width * 2))
        .attr("y", (h / 2) - (bar_height / 4))
        .attr("width", filled_width)
        .attr("height", bar_height / 2)
        .attr("fill", filled_color);

    // Get x value from circle's cx
    function get_x_value(bar) {
        return x_scale.invert(bar.attr("x"));
    }

    // Drag functions
    function dragged_start_bar(event) {
        // Get proposed new value
        var current_value = x_scale.invert(event.x);
        // Limit based on end circle value
        var end_bar_value = get_x_value(end_bar);
        current_value = Math.min(current_value, end_bar_value - scaled_bar * 2);
        // Update start circle
        start_bar.attr("x", x_scale(current_value));
        show_fcn(matrix, current_value, "fcn_graph_start_" + id_number, id_number);
        const msg = `Selected range: [${current_value}, ${end_bar_value})`;
        $("#fcn_" + id_number).text(msg);
        // Update filled area
        filled_area.attr("x", parseFloat(start_bar.attr("x")) + bar_width * 2)
            .attr("width", parseFloat(end_bar.attr("x")) - parseFloat(start_bar.attr("x")) - (bar_width * 2));

    }

    function dragged_end_bar(event) {

        // Get proposed new value
        var current_value = x_scale.invert(event.x);
        // Limit based on start circle value
        var start_bar_value = get_x_value(start_bar);
        current_value = Math.max(current_value, start_bar_value + scaled_bar * 2);
        // Update end circle
        end_bar.attr("x", x_scale(current_value));
        show_fcn(matrix, current_value, "fcn_graph_end_" + id_number, id_number);
        const msg = `Selected range: [${start_bar_value}, ${current_value})`;
        $("#fcn_" + id_number).text(msg);
        // Update filled area
        filled_area.attr("x", parseFloat(start_bar.attr("x")) + bar_width * 2)
            .attr("width", parseFloat(end_bar.attr("x")) - parseFloat(start_bar.attr("x")) - (bar_width * 2));

    }

    // Append the SVG element to the container
    slider_container.node().append(slider_svg.node());
}

function show_fcn(matrix, max_distance, html_element_id, id_number) {
    const epsilon = 1e-5;
    $("#" + html_element_id).empty();
    const position = html_element_id.split("_")[2];
    let fcn_title = `${position} threshold ${max_distance}`;
    max_distance += epsilon;
    $("#" + html_element_id + "_title").text(fcn_title);
    const fcn_container = d3.select("#" + html_element_id);
    // Declare the chart dimensions and margins.
    const width = fcn_container.node().getBoundingClientRect().width;
    const height = 300;
    const margin_top = 5;
    const margin_right = 5;
    const margin_bottom = 5;
    const margin_left = 5;
    // Create the SVG container.
    const fcn_svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [-width / 2, -height / 2, width, height])
        .attr("style", "max-width: 100%; height: auto;");

    let nodes = [];
    for (let i = 0; i < matrix.length; i++) {
        nodes.push({id: i, name: i.toString()});
    }

    let links = [];
    for (let i = 0; i < matrix.length; i++) {
        for (let j = i + 1; j < matrix[i].length; j++) {
            if ((matrix[i][j] !== 0) && (matrix[i][j] <= max_distance)) {
                links.push({source: i, target: j, value: matrix[i][j]});
            }
        }
    }

    // Create a simulation with several forces.
    const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id))
        .force("charge", d3.forceManyBody().strength(-37)) // Adjust charge strength
        .force("x", d3.forceX().strength(0.20)) // Adjust forceX strength
        .force("y", d3.forceY().strength(0.20)); // Adjust forceY strength

    // Add zoom functionality
    const zoom = d3.zoom()
        .scaleExtent([1, 10])
        .on("zoom", zoomed);

    function zoomed(event) {
        fcn_svg.selectAll('g').attr('transform', event.transform);
        simulation.restart();
    }

    fcn_svg.call(zoom);

    // Add drag functionality
    const drag = d3.drag()
        .on("start", (event, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        })
        .on("drag", (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
        })
        .on("end", (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        });
    // Add a line for each link, and a circle for each node.
    const link = fcn_svg.append("g")
        .attr("stroke", bar_hover_color)
        .attr("stroke-opacity", 0.9)
        .selectAll("line")
        .data(links)
        .join("line")
        .attr("stroke-width", 2);

    const node = fcn_svg.append("g")
        .selectAll("g")
        .data(nodes)
        .join("g")
        .call(drag) // Enable drag
        .on("mouseover", function (event, d) {
            const current_element = d3.select(this);
            const msg = `Node ${d.id}`;
            $(this).tooltip({
                title: msg,
                placement: "top",
                trigger: "manual"
            }).tooltip("show");
        })
        .on("mouseout", function (d) {
            const current_element = d3.select(this);
            const tooltip_element = $(this);
            setTimeout(function () {
                tooltip_element.tooltip("hide");
            }, 100);
        });

    node.append("circle")
        .attr("r", 8)
        .attr("fill", bar_color)
        .style("stroke-width", 1);


    node.append("text")
        .style("text-anchor", "middle")
        .attr("y", 3)
        .style("stroke", "white")
        .style("font-size", "8px")
        .style("stroke-width", 1)
        .style("pointer-events", "none")
        .text(function (d) {
            return d.id
        });


    // Set the position attributes of links and nodes each time the simulation ticks.
    simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);
        node
            .attr("transform", d => `translate(${d.x}, ${d.y})`);
    });
    fcn_container.node().append(fcn_svg.node());

}

async function read_file(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = function (e) {
            const content = e.target.result;
            let matrix;
            if (file.name.endsWith(".csv")) {
                matrix = d3.csvParseRows(content, (row) => row.map((value) => +value));
            } else if (file.name.endsWith(".tsv") || file.name.endsWith(".txt")) {
                matrix = d3.tsvParseRows(content, (row) => row.map((value) => +value));
            } else {
                reject(new Error("Unsupported file format"));
            }
            resolve(matrix);
        };

        reader.readAsText(file);
    });
}


function after_computation(matrix, panel_id) {
    let barcodes = [];
    $('#diagram_' + panel_id + ' svg rect').each(function () {
        const title = $(this).find('title');
        if (title.length > 0) {
            const values = title.text().replace(/[\[\],)]/g, '').replace(/[\s]/g, '-').split('-');
            barcodes.push([parseFloat(values[0]), parseFloat(values[1])]);
        }
    });
    show_barcode(barcodes, matrix, panel_id);
    show_fcn(matrix, 0, "fcn_graph_start_" + panel_id, panel_id);
    show_fcn(matrix, 0, "fcn_graph_end_" + panel_id, panel_id);
}

function perform_data_change(matrix, dimension, panel_id) {
    $("#output_" + panel_id).show();
    // Empty the existing diagram content which is generated by ripser
    $("#diagram_" + panel_id).empty();
    $("#fcn_" + panel_id).empty();

    show_slider(matrix, 0, 0, panel_id);

    const ripser_options = {
        format: "distance",
        minDim: dimension,
        maxDim: dimension,
        callback: after_computation.bind(null, matrix, panel_id)
    };
    Ripser.run(matrix, "#diagram_" + panel_id, ripser_options);
}

function show_dataset_info(panel_id, filename) {
    let dataset_info = '(Loaded <span class="badge bg-secondary">' + filename + '</span> dataset)';
    $("#dataset_info_" + panel_id).html(dataset_info);
}

function show_charts(dimension, file_matrix, panel_id, show_example = 0) {
    const file_1 = "data/ph_data/subject_1_mx645.txt";
    const file_2 = "data/ph_data/subject_1_mx1400.txt";
    const file_3 = "data/ph_data/subject_1_std2500.txt";

    $("#dimension_value_" + panel_id).text(dimension);
    let file = "data/temporal_data/normalize_dfc_2500_subject_1_time_1.txt";
    if (panel_id == 1) {
        file = file_1;
    } else if (panel_id == 2) {
        file = file_2;
    } else if (panel_id == 3) {
        file = file_3;
    }
    if ((file && show_example === 1) || (file && file_matrix === null)) {
        show_dataset_info(panel_id, file);
        get_static_data(file).then(function (matrix) {
            perform_data_change(matrix, dimension, panel_id);
        }).catch(function (error) {
            console.error(error.message);
        });
    } else if (file_matrix !== null) {
        perform_data_change(file_matrix, dimension, panel_id);
    }
}


