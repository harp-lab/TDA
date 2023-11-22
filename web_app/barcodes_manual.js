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

// function get_holes(matrix, min_distance) {
//     const holes = [];
//     const number_of_nodes = matrix.length;
//     const seen = new Set();
//
//     function dfs(node, parent, hole) {
//         seen.add(node);
//         hole.push(node);
//
//         for (let neighbor = 0; neighbor < number_of_nodes; neighbor++) {
//             if (matrix[node][neighbor] <= min_distance) {
//                 if (!seen.has(neighbor)) {
//                     dfs(neighbor, node, hole);
//                 } else if (neighbor !== parent && hole.indexOf(neighbor) !== -1) {
//                     // Found a hole (cycle)
//                     holes.push(hole.slice(hole.indexOf(neighbor)));
//                 }
//             }
//         }
//     }
//
//     for (let i = 0; i < number_of_nodes; i++) {
//         if (!seen.has(i)) {
//             const hole = [];
//             dfs(i, -1, hole);
//         }
//     }
//
//     return holes;
// }
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

function manual_show() {
    $("#output").show();
    let file = "../data/demo_data.txt";
    file = "../data/fmri_data/normalize_dfc_2500_subject_1_time_1.txt";
    if (file) {
        get_static_data(file).then(function (matrix) {
            $("#barcodes").empty();
            const barcodes = get_0_dim_barcodes(matrix);
            show_barcode(barcodes, matrix);
            $("#fcn_graph_start").empty();
            $("#fcn_graph_end").empty();
            show_fcn(matrix, 0, "fcn_graph_start");
            show_fcn(matrix, 0, "fcn_graph_end");
        }).catch(function (error) {
            console.error(error.message);
        });
    }
}
