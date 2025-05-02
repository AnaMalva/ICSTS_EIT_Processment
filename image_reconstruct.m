run("C:/Users/anama/OneDrive/Ambiente de Trabalho/UNI/Semestre2/ICSTS/Task3/eidors-v3.12-ng/eidors/startup.m")

%%
data=struct;

for i = 1:78
    disp(i)

    if i <= 9
        folderPath = "C:/Users/anama/OneDrive/Ambiente de Trabalho/UNI/Semestre2/ICSTS/Task3/BRACETS Bimodal Repository of Auscultation Coupled with Electrical Impedance Thoracic Signals/BRACETS/Data/0" + int2str(i) + "/EIT";
    else
        folderPath = "C:/Users/anama/OneDrive/Ambiente de Trabalho/UNI/Semestre2/ICSTS/Task3/BRACETS Bimodal Repository of Auscultation Coupled with Electrical Impedance Thoracic Signals/BRACETS/Data/" + int2str(i) + "/EIT";
    end

    files = dir(fullfile(folderPath, '*.eit'));

    for file_num = 1:length(files)
        file_data=[];
        file_data=[file_data,eidors_readdata(fullfile(folderPath, files(file_num).name),"eit")];
        data.("set" + int2str(i)).("trial"+int2str(file_num)) = file_data;
    end
end

%%

fmdl= mk_library_model('adult_male_16el_lungs');
fmdl.electrode = fmdl.electrode([9:16,1:8]);
img = mk_image(fmdl, 1); % background conductivity
img.elem_data([fmdl.mat_idx{2};fmdl.mat_idx{3}]) = 0.3; % lungs
figure;
subplot(211); show_fem(img);
print_convert adult_ex01a.png
figure;show_fem(img,[0,1]); view(2); %electrode #'s
print_convert adult_ex01b.png

%%

[stim,msel] = mk_stim_patterns(16,1,[0,1],[0,1],{'no_meas_current'},1);
img.fwd_model.stimulation = stim;
img.fwd_model = mdl_normalize(img.fwd_model, 1);
opt.imgsz = [32 32];
opt.distr = 3; % non-random, uniform
opt.Nsim = 500; % 500 hundred targets to train on, seems enough
opt.target_size = 0.03; %small targets
opt.target_offset = 0;
opt.noise_figure = .5; % this is key!
opt.square_pixels = 1;
imdl=mk_GREIT_model(img, 0.25, [], opt);
imdl.fwd_model.meas_select = msel;

%%

for set=1:9

    folderPath = "C:/Users/anama/OneDrive/Ambiente de Trabalho/UNI/Semestre2/ICSTS/Task3/BRACETS Bimodal Repository of Auscultation Coupled with Electrical Impedance Thoracic Signals/BRACETS/Data/0" + int2str(i) + "/EIT";

    files = dir(fullfile(folderPath, '*.eit'));

    disp(set)
    disp('---------------------------')
   for trial = 1:length(files)
        
        disp(trial)
        zc_resp=data.("set" + int2str(set)).("trial"+int2str(trial));
        img= inv_solve(imdl, zc_resp(:,1), zc_resp);

        num_frames = size(get_img_data(img), 2);

        % Create a folder to save images for this trial
        output_folder = sprintf('set_%02d/trial_%02d', set, trial);
        if ~exist(output_folder, 'dir')
            mkdir(output_folder);
        end

        for i=1:num_frames
            figure
            img.calc_colours.ref_level = 0;
            img.get_img_data.frame_select = i;
            show_fem(img);
            filename = fullfile(output_folder, sprintf('frame_%03d.png', i));
            saveas(gcf, filename);  % Save the current figure, not the img object
            close(gcf) 
        end
    end
end

%%
for set=10:78
    
    folderPath = "C:/Users/anama/OneDrive/Ambiente de Trabalho/UNI/Semestre2/ICSTS/Task3/BRACETS Bimodal Repository of Auscultation Coupled with Electrical Impedance Thoracic Signals/BRACETS/Data/" + int2str(set) + "/EIT";

    files = dir(fullfile(folderPath, '*.eit'));

    disp(set)
    disp('---------------------------')

    for trial = 1:length(files)

        init=1

        set_field = "set" + int2str(set);
        trial_field = "trial" + int2str(trial);

        if ~isfield(data, set_field) || ~isfield(data.(set_field), trial_field)
            disp(['Skipping trial ', trial_field, ' for set ', set_field, ' (data not found)']);
            continue  % Skip to next trial
        end

        disp(trial)
        zc_resp=data.("set" + int2str(set)).("trial"+int2str(trial));
        img= inv_solve(imdl, zc_resp(:,1), zc_resp);

        num_frames = size(get_img_data(img), 2);

        % Create a folder to save images for this trial
        output_folder = sprintf('set_%02d/trial_%02d', set, trial);
        if ~exist(output_folder, 'dir')
            mkdir(output_folder);
        end

        if trial==1
            init=487;
        end

        for i=init:num_frames
            figure
            img.calc_colours.ref_level = 0;
            img.get_img_data.frame_select = i;
            show_fem(img);
            filename = fullfile(output_folder, sprintf('frame_%03d.png', i));
            saveas(gcf, filename);  % Save the current figure, not the img object
            close(gcf) 
        end
    end
end
