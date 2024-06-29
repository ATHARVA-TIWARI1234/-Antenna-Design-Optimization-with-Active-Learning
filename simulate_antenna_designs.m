clear;
    clc;
    tic;
    % Default settings
    pxSize = 0.005; % Pixel size in meters
    gridSize = 6;   % Number of grid-cells/pixels along one dimension

    % Read the patch coordinates and counts from the text files
    patchCoords = readmatrix('patchcoords.txt');
   
    
    % Antenna parameters
    er = 4.4; % Dielectric constant
    thick = 1.6e-3; % Substrate thickness
    pcbLen = gridSize * pxSize + 0.5e-3; % PCB length
    pcbWid = gridSize * pxSize + 0.5e-3; % PCB width

    % Frequency range for S11
    freq = linspace(1e9, 6e9, 128); % Frequency range from 1 to 6 GHz
    azi = linspace(0, 360, 25);
    % elev = linspace(0, 180, 13);

    n = size(patchCoords,1)/36;
    % Initialize array for S-parameters in dB
    S11_data = zeros(n, length(freq));
    % sparams_all = zeros(length(freq), n);
    pattern_data = zeros(n, length(freq), 25, 13);
    

    % Design loop
    parfor i = 1:40

        startIndex = (i-1)*36 +1;
        
        % Substrate setup
        d = dielectric('FR4');
        d.EpsilonR = er;
        d.Thickness = thick;

        % Ground plane setup
        GndPlane = antenna.Rectangle('Length', pcbLen, 'Width', pcbWid);

        % Top layer setup, initializing with a dummy rectangle
        r = antenna.Rectangle('Length', 1e-6, 'Width', 1e-5, 'Center', [0, 0]);

        endIndex = startIndex + 35;

        % disp(['startIndex: ', num2str(startIndex), ', endIndex: ', num2str(endIndex)]);

        % Create patches on the PCB using coordinates from file
        for idx = startIndex:endIndex
            cx = patchCoords(idx, 1);
            cy = patchCoords(idx, 2);
            dx = patchCoords(idx, 3);
            dy = patchCoords(idx, 4);

            % Validate dx and dy
            if dx > 0 && dy > 0
                % Create and add each rectangle to the top layer
                rect = antenna.Rectangle('Length', dx, 'Width', dy, 'Center', [cx, cy]);
                r = r + rect;
            end
            
        end

        % PCB stack setup
        p = pcbStack;
        p.Name = 'Multilayer Antenna';
        p.BoardShape = GndPlane;
        p.BoardThickness = thick;
        p.Layers = {r, d, GndPlane}; % Layer setup
        xfeed = 1.5e-3;
        yfeed = -gridSize * pxSize/2 + 1.5e-3;
        p.FeedLocations = [xfeed, yfeed, 3, 1];

        % Uncomment the following lines to visualize the antenna
        %figure;
        %show(p);
        % for f = 1:128
            % freq = linspace(1e9, 6e9, 128);
            % Calculate S-parameters
            s = sparameters(p, freq);
            s11 = rfparam(s, 1, 1);
            S11_data(i, :) = mag2db(abs(s11));
            for m = 1:13
                elev = (m - 1) * 180 / 12; 
                pattern_data(i,:, :, m) = pattern(p, freq, azi, elev);
            end

       
        disp(['Iteration No: ', num2str(i)]); 
        
        
    end

    % Save S-parameters to a text file
   
    writematrix(S11_data, 'sparameters_trial.txt', 'Delimiter', 'tab');
    writematrix(pattern_data, 'Rad_pattern_trial.txt', 'Delimiter', 'tab');
    
    toc;
% end