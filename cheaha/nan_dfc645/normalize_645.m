data = load("dynamic_FC_645.mat");

conn_dfc = data.conn_dfc_data_645_all;
count = 0;
[number_of_time_points, number_of_rois_1, number_of_rois_2, number_of_subjects] = size(conn_dfc);
for i = 1:1
    M = zeros(number_of_time_points, number_of_rois_1, number_of_rois_2);
    for j = 1:number_of_rois_1
        for k = 1:number_of_rois_2
            for l = 1:number_of_time_points
                current_val = conn_dfc(l, j, k, i);
                q = isnan(current_val);
                if(q == 1) 
                    current_val = 0;
                    disp(current_val);
                end
                M(l, j, k) = current_val;
            end
        end
    end
    for j = 1:number_of_time_points
        filename = "dfc_645_normal_nonan/normalize_dfc_645_subject_" + i + "_time_"+j+".txt";
        time_data = reshape(M(j,:,:), [number_of_rois_1, number_of_rois_2]);
        subject_data = corrcoef(transpose(time_data));
        subject_data_normalize = sqrt(1 - subject_data.*subject_data);
        writematrix(subject_data_normalize, filename, 'Delimiter', 'tab');
        %disp("Done writing "+filename);
        count = count + 1;
    end
end
disp("Number of time points: " + number_of_time_points);
disp("ROI 1: "+number_of_rois_1);
disp("ROI 2: "+number_of_rois_2);
disp("Number of subjects: " + number_of_subjects);
disp("Total wrote "+count+" files");

