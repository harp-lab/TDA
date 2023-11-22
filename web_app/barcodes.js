async function get_static_data(file_path) {
    let data_file = "../data/fmri_data/normalize_dfc_2500_subject_1_time_1.txt";
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
    const container = d3.select("#barcodes");
    // Remove existing SVG content
    container.selectAll("svg").remove();
    // Declare the chart dimensions and margins.
    const width = container.node().getBoundingClientRect().width;
    const margin_top = 20;
    const margin_right = 20;
    const margin_bottom = 20;
    const margin_left = 20;
    const bar_height = 10; // Fixed height for the bars

    const bar_color = "#001E62";
    const bar_hover_color = "#D50032";
    const bar_click_color = "#FFBF3F";

    // Calculate the height of the SVG container based on the number of bars
    const height = barcodes.length * (bar_height + 5) + margin_top + margin_bottom;
    const padding = 5;
    // Sort data by the length of the ranges (largest to smallest)
    barcodes.sort((a, b) => (b[1] - b[0]) - (a[1] - a[0]));
    // // Sort data by the second element of each sub-array (largest to smallest)
    // barcodes.sort((a, b) => b[1] - a[1]);
    // Calculate the maximum value in the matrix
    const maxValue = matrix.reduce((max, row) => Math.max(max, ...row), Number.NEGATIVE_INFINITY);


    // Create scales for x and y axes
    const xScale = d3.scaleLinear()
        .domain([0, maxValue])
        .range([margin_left, width]);

    const yScale = d3.scaleBand()
        .domain(d3.range(barcodes.length))
        .range([margin_top + padding, height - margin_bottom])
        .padding(0.1);

    // Create the SVG container.
    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height);

    // Create horizontal bars
    svg.selectAll("rect")
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
            if (current_element.attr("clicked") === "false") {
                $(".bar").attr("fill", bar_color);
                $(".bar").attr("clicked", "false");
                current_element.attr("fill", bar_click_color);
                current_element.attr("clicked", "true");
                const bar_start = d3.format(".3f")(d[0]);
                const bar_end = d3.format(".3f")(d[1]);
                const msg = `Selected barcode: [${d[0]}, ${bar_end})`;
                $("#fcn_graph_start").empty();
                $("#fcn_graph_end").empty();
                $("#fcn").text(msg);
                show_fcn(matrix, bar_start, "fcn_graph_start");
                show_fcn(matrix, bar_end, "fcn_graph_end");
            } else {
                current_element.attr("fill", bar_color);
                current_element.attr("clicked", "false");
                $("#fcn").empty();
                $("#fcn_graph_start").empty();
                $("#fcn_graph_end").empty();
                show_fcn(matrix, 0, "fcn_graph_start");
                show_fcn(matrix, 0, "fcn_graph_end");
            }
        });

    // Add the x-axis.
    svg.append("g")
        .attr("transform", `translate(0,${margin_top})`)
        .call(d3.axisTop(xScale));


    // Append the SVG element to the container
    container.node().append(svg.node());
    // container.html(svg.node().outerHTML);
}

function show_fcn(matrix, max_distance, html_element_id) {
    // Select the container with id "barcodes"
    $("#" + html_element_id).empty();
    $("#" + html_element_id+"_title").text("Maximum distance "+max_distance);
    const container = d3.select("#" + html_element_id);
    const bar_color = "#001E62";
    const bar_hover_color = "#D50032";
    const bar_click_color = "#FFBF3F";
    // Declare the chart dimensions and margins.
    const width = container.node().getBoundingClientRect().width;
    const height = 700;
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
        .force("charge", d3.forceManyBody().strength(-150)) // Adjust charge strength
        .force("x", d3.forceX().strength(0.2)) // Adjust forceX strength
        .force("y", d3.forceY().strength(0.2)); // Adjust forceY strength


    // Add a line for each link, and a circle for each node.
    const link = svg.append("g")
        .attr("stroke", bar_hover_color)
        .attr("stroke-opacity", 0.6)
        .selectAll("line")
        .data(links)
        .join("line")
        .attr("stroke-width", 3);

    const node = svg.append("g")
        .attr("stroke", "#fff")
        .attr("stroke-width", 1.5)
        .selectAll("circle")
        .data(nodes)
        .join("circle")
        .attr("r", 7)
        .attr("fill", bar_color)
        .on("mouseover", function (event, d) {
            const current_element = d3.select(this);
            const msg = `node ${d.id}`;
            current_element.style("cursor", "pointer");
            $(this).tooltip({
                title: msg,
                placement: "top",
                trigger: "manual"
            }).tooltip("show");
        })
        .on("mouseout", function (d) {
            const current_element = d3.select(this);
            current_element.style("cursor", "auto");
            // Use Bootstrap's tooltip hide with a delay
            const tooltip_element = $(this);
            setTimeout(function () {
                tooltip_element.tooltip("hide");
            }, 100);
        })

    // Set the position attributes of links and nodes each time the simulation ticks.
    simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);
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

function default_show(dimension) {
    $("#output").show();
    let file = "../data/demo_data.txt";
    file = "../data/fmri_data/normalize_dfc_2500_subject_1_time_1.txt";
    if (file) {
        get_static_data(file).then(function (matrix) {
            const ripser_options = {
                // outputType: 'PersistenceDiagram',
                format: "distance",
                minDim: dimension,
                maxDim: dimension,
                callback: after_computation.bind(null, matrix)
            };
            Ripser.run(matrix, "#diagram", ripser_options);
        }).catch(function (error) {
            console.error(error.message);
        });
    }
}


