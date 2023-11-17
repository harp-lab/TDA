function get_unique_distances(matrix) {
    const unique_distances = new Set();
    for (let i = 0; i < matrix.length; i++) {
        for (let j = i + 1; j < matrix.length; j++) {
            unique_distances.add(matrix[i][j]);
        }
    }
    const distances = Array.from(unique_distances);
    distances.sort();
    return distances;
}

function get_components(matrix, min_distance) {
    const components = [];
    const number_of_nodes = matrix.length;
    const seen = new Set();
    for (let i = 0; i < number_of_nodes; i++) {
        if (!seen.has(i)) {
            let component = [];
            let visited = new Array(number_of_nodes).fill(false);
            let queue = [i];
            visited[i] = true;
            while (queue.length !== 0) {
                const current_node = queue.shift();
                seen.add(current_node);
                component.push(current_node);
                for (let node = 0; node < number_of_nodes; node++) {
                    if (visited[node] === false && (matrix[current_node][node] <= min_distance)) {
                        queue.push(node);
                        visited[node] = true;
                    }
                }
            }
            components.push(component);
        }
    }
    return components;
}

async function get_static_data() {
    let data_file = "../data/fmri_data/normalize_dfc_2500_subject_1_time_1.txt";
    // data_file = "../data/demo_data.txt";
    // data_file = "../data/time_varying_4_4.csv";
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

function get_0_dim_barcodes(matrix) {
    const number_of_nodes = matrix.length;
    let barcodes = [];
    const unique_distances = get_unique_distances(matrix);
    const max_distance = unique_distances[unique_distances.length - 1];
    let prev_number_of_components = -1;
    for (let i = 0; i < unique_distances.length; i++) {
        const distance = unique_distances[i];
        const components = get_components(matrix, distance);
        const number_of_components = components.length;
        if (number_of_components === 1) {
            barcodes.push([0, distance, components]);
            break;
        }
        if (prev_number_of_components === -1) {
            prev_number_of_components = number_of_components;
            barcodes.push([0, distance, components]);
            continue;
        }
        if (number_of_components < prev_number_of_components) {
            for (let i = 0; i < (prev_number_of_components - number_of_components); i++) {
                barcodes.push([0, distance, components]);
            }
            prev_number_of_components = number_of_components;
        }
    }
    const remaining_bars = number_of_nodes - barcodes.length;
    const components = get_components(matrix, max_distance);
    for (let i = 0; i < remaining_bars; i++) {
        barcodes.push([0, max_distance, components]);
    }
    return barcodes;
}

function show_barcode(data) {
    // Select the container with id "barcodes"
    const container = d3.select("#barcodes");

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
    const height = data.length * (bar_height + 5) + margin_top + margin_bottom;
    const padding = 5;
    // Sort data by the second element of each sub-array (largest to smallest)
    data.sort((a, b) => b[1] - a[1]);
    // Calculate the maximum value in the data array
    const maxValue = d3.max(data, d => d[1]);

    // Create scales for x and y axes
    const xScale = d3.scaleLinear()
        .domain([0, maxValue])
        .range([margin_left, width]);

    const yScale = d3.scaleBand()
        .domain(d3.range(data.length))
        .range([margin_top + padding, height - margin_bottom])
        .padding(0.1);

    // Create the SVG container.
    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height);

    // Create horizontal bars
    svg.selectAll("rect")
        .data(data)
        .enter().append("rect")
        .attr("x", margin_left)
        .attr("y", (d, i) => yScale(i))
        .attr("width", d => xScale(d[1]))
        .attr("height", bar_height)
        .attr("fill", bar_color)
        .attr("clicked", "false")
        .attr("class", "bar")
        .on("mouseover", function (event, d) {
            const current_element = d3.select(this);
            if (current_element.attr("clicked") === "false") {
                current_element.attr("fill", bar_hover_color);
            }
            const bar_end = d3.format(".3f")(d[1]);
            const msg = `[${d[0]}, ${bar_end}), ${d[2].length} components`;
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
            // d3.select(this).attr("fill", bar_click_color);
            const current_element = d3.select(this);
            if (current_element.attr("clicked") === "false") {
                $(".bar").attr("fill", bar_color);
                $(".bar").attr("clicked", "false");
                current_element.attr("fill", bar_click_color);
                current_element.attr("clicked", "true");
                const bar_end = d3.format(".3f")(d[1]);
                const msg = `[${d[0]}, ${bar_end}), ${d[2].length} components`;
                $("#fcn").text(msg);
            } else {
                current_element.attr("fill", bar_color);
                current_element.attr("clicked", "false");
                $("#fcn").text("");
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

function show_fcn(adjacencyMatrix, barcodes) {
    // Select the container with id "barcodes"
    const container = d3.select("#fcn_graph");

    // Declare the chart dimensions and margins.
    const width = container.node().getBoundingClientRect().width;
    const height = 500;
    const margin_top = 20;
    const margin_right = 20;
    const margin_bottom = 20;
    const margin_left = 20;
    // Create the SVG container.
    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height);

    var links = [];
    for (var i = 0; i < adjacencyMatrix.length; i++) {
        for (var j = i + 1; j < adjacencyMatrix[i].length; j++) {
            if (adjacencyMatrix[i][j] !== 0) {
                links.push({source: i, target: j, weight: adjacencyMatrix[i][j]});
            }
        }
    }

    // Create links
    var linkSelection = svg.selectAll("line")
        .data(links)
        .enter()
        .append("line")
        .style("stroke", "black");

    // Create nodes
    var nodeSelection = svg.selectAll("circle")
        .data(d3.range(adjacencyMatrix.length))
        .enter()
        .append("circle")
        .attr("r", 5)
        .attr("cx", function (d, i) {
            return Math.cos(2 * Math.PI * i / adjacencyMatrix.length) * 150 + 200;
        })
        .attr("cy", function (d, i) {
            return Math.sin(2 * Math.PI * i / adjacencyMatrix.length) * 150 + 200;
        })
        .style("fill", "blue")
        .style("cursor", "pointer")
        .on("mouseover", function (event, d) {
            // Add tooltip or any other action on mouseover
            d3.select(this).style("fill", "red");
        })
        .on("mouseout", function (event, d) {
            // Reset to original color on mouseout
            d3.select(this).style("fill", "blue");
        });

    // Create labels for weights
    // var textSelection = svg.selectAll("text")
    //     .data(links)
    //     .enter()
    //     .append("text")
    //     .attr("x", function (d) {
    //         return (nodeSelection.data()[d.source].cx + nodeSelection.data()[d.target].cx) / 2;
    //     })
    //     .attr("y", function (d) {
    //         return (nodeSelection.data()[d.source].cy + nodeSelection.data()[d.target].cy) / 2;
    //     })
    //     .text(function (d) {
    //         return d.weight;
    //     })
    //     .attr("text-anchor", "middle")
    //     .attr("dominant-baseline", "middle");

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

$("#data_file").on("change", function (event) {
        $("#output").show();

        const file = event.target.files[0];

        if (file) {
            $("#barcodes").empty();
            $("#fcn").empty();
            read_file(file).then(function (matrix) {
                const barcodes = get_0_dim_barcodes(matrix);
                show_barcode(barcodes);
                // show_fcn(matrix, barcodes);
            }).catch(function (error) {
                console.error(error.message);
            });
        }
    }
)

$(document).ready(function () {
    $("#output").hide();
});
