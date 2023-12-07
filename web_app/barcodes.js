var bar_color = "#001E62";
var bar_hover_color = "#D50032";
var bar_click_color = "#FFBF3F";


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
        return matrix;
    });
}


function show_barcode(barcodes, matrix) {
    $("#barcodes").empty();
    // Select the container with id "barcodes"
    const barcodes_container = d3.select("#barcodes");
    // Remove existing SVG content
    barcodes_container.selectAll("svg").remove();
    // Declare the chart dimensions and margins.
    const margin_top = 20;
    const margin_right = 20;
    const margin_bottom = 20;
    const margin_left = 20;
    const width = barcodes_container.node().getBoundingClientRect().width - 30;
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
            $("#fcn").empty();
            $("#fcn_graph_start").empty();
            $("#fcn_graph_end").empty();
            if (current_element.attr("clicked") === "false") {
                $(".bar").attr("fill", bar_color);
                $(".bar").attr("clicked", "false");
                current_element.attr("fill", bar_click_color);
                current_element.attr("clicked", "true");
                const msg = `Selected barcode: [${d[0]}, ${d[1]})`;
                $("#fcn").text(msg);
                show_fcn(matrix, d[0], "fcn_graph_start");
                show_fcn(matrix, d[1], "fcn_graph_end");
                show_slider(matrix, d[0], d[1]);
            } else {
                current_element.attr("fill", bar_color);
                current_element.attr("clicked", "false");
                show_fcn(matrix, 0, "fcn_graph_start");
                show_fcn(matrix, 0, "fcn_graph_end");
                show_slider(matrix, d[0], d[1]);
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

function show_slider(matrix, start_value = 0, end_value = 0) {
    // Flatten the matrix
    let flattened_values = matrix.flat();

    // Get unique values using Set
    let values = [...new Set(flattened_values)].sort();

    $("#slider-container").empty();
    // Select the container with id "barcodes"
    const slider_container = d3.select("#slider-container");
    // Remove existing SVG content
    slider_container.selectAll("svg").remove();
    // Width and height
    const w = slider_container.node().getBoundingClientRect().width - 30;
    const h = 35;
    const min_value = d3.min(values);
    const max_value = d3.max(values);
    if (start_value === 0 && end_value === 0) {
        const msg = `Selected range: [0, 0)`;
        $("#fcn").text(msg);
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
        show_fcn(matrix, current_value, "fcn_graph_start");
        const msg = `Selected range: [${current_value}, ${end_bar_value})`;
        $("#fcn").text(msg);
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
        show_fcn(matrix, current_value, "fcn_graph_end");
        const msg = `Selected range: [${start_bar_value}, ${current_value})`;
        $("#fcn").text(msg);
        // Update filled area
        filled_area.attr("x", parseFloat(start_bar.attr("x")) + bar_width * 2)
            .attr("width", parseFloat(end_bar.attr("x")) - parseFloat(start_bar.attr("x")) - (bar_width * 2));

    }

    // Append the SVG element to the container
    slider_container.node().append(slider_svg.node());
}

function show_fcn(matrix, max_distance, html_element_id) {
    const epsilon = 1e-5;
    $("#" + html_element_id).empty();
    const position = html_element_id.split("_").pop();
    let fcn_title = `${position} threshold ${max_distance}`;
    max_distance += epsilon;
    $("#" + html_element_id + "_title").text(fcn_title);
    const container = d3.select("#" + html_element_id);
    // Declare the chart dimensions and margins.
    const width = container.node().getBoundingClientRect().width;
    const height = 600;
    const margin_top = 20;
    const margin_right = 20;
    const margin_bottom = 20;
    const margin_left = 20;
    // Create the SVG container.
    const svg = d3.create("svg")
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
        .force("charge", d3.forceManyBody().strength(-135)) // Adjust charge strength
        .force("x", d3.forceX().strength(0.2)) // Adjust forceX strength
        .force("y", d3.forceY().strength(0.2)); // Adjust forceY strength


    // Add a line for each link, and a circle for each node.
    const link = svg.append("g")
        .attr("stroke", bar_hover_color)
        .attr("stroke-opacity", 0.6)
        .selectAll("line")
        .data(links)
        .join("line")
        .attr("stroke-width", 2);

    const node = svg.append("g")
        .selectAll("g")
        .data(nodes)
        .join("g")
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
        .attr("r", 12)
        .attr("fill", bar_color)
        .style("stroke-width", 1);


    node.append("text")
        .style("text-anchor", "middle")
        .attr("y", 3)
        .style("stroke", "white")
        .style("font-size", "10px")
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
    container.node().append(svg.node());

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


function after_computation(matrix) {
    let barcodes = [];
    $('#diagram svg rect').each(function () {
        const title = $(this).find('title');
        if (title.length > 0) {
            const values = title.text().replace(/[\[\],)]/g, '').replace(/[\s]/g, '-').split('-');
            barcodes.push([parseFloat(values[0]), parseFloat(values[1])]);
        }
    });
    show_barcode(barcodes, matrix);
    show_fcn(matrix, 0, "fcn_graph_start");
    show_fcn(matrix, 0, "fcn_graph_end");
}

function perform_data_change(matrix, dimension) {
    $("#output").show();
    // Empty the existing diagram content which is generated by ripser
    $("#diagram").empty();
    $("#fcn").empty();

    show_slider(matrix);

    const ripser_options = {
        format: "distance",
        minDim: dimension,
        maxDim: dimension,
        callback: after_computation.bind(null, matrix)
    };
    Ripser.run(matrix, "#diagram", ripser_options);
}

function show_charts(dimension, file_matrix) {
    $("#dimension_value").text(dimension);
    let file = "data/demo_data.txt";
    file = "data/fmri_data/normalize_dfc_2500_subject_1_time_1.txt";
    if (file && file_matrix === null) {
        get_static_data(file).then(function (matrix) {
            perform_data_change(matrix, dimension);
        }).catch(function (error) {
            console.error(error.message);
        });
    } else if (file_matrix !== null) {
        perform_data_change(file_matrix, dimension);
    }
}


