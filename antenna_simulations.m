function simulate()


    
    gridSize = 6;   % Number of grid-cells/pixels along one dimension


    n_4 = 200; % no of designs with pixel size 4mm
    n_45 = 200; % no of designs with pixel size 4.5mm
    n_5 = 300; % no of designs with pixel size 5mm
    n_575 = 500; % no of designs with pixel size 5.75mm
    n_6 = 0; % no of designs with pixel size 6mm
    

    n = n_4 + n_45 + n_5 + n_575 + n_6; % Number of antenna designs


    % Read the patch coordinates and counts from the text files
    patchCoords = readmatrix('patchcoords.txt');
    

    % Antenna parameters
    er = 4.4; % Dielectric constant
    thick = 1.6e-3; % Substrate thickness


    % Frequency range for S11
    freq = linspace(1e9, 6e9, 128); % Frequency range from 1 to 6 GHz


    % Initialize array for S-parameters in dB
    sparams_all = zeros(n, length(freq));


    % Design loop
    for i = 1:n
        tic;
        

        startIndex = (i-1) * 36 + 1;
        endIndex = startIndex + 35;

        if i>0 && i<=n_4
            pxSize = 0.004; % Pixel size in meters
        end
        if i>=n_4+1 && i<=n_4 + n_45
            pxSize = 0.005; % Pixel size in meters
        end
        
        if i>=n_4+n_45+1 && i<= n_4 + n_45 + n_5
            pxSize = 0.005; % Pixel size in meters
        end
        if i>=n_4+n_45+n_5+1 && i<= n_4+n_45+n_5+n_575
            pxSize = 0.00575;
        end
        if i>=n_4+n_5+n_575+1 && i<= n_4 + n_5 + n_575+n_6
            pxSize = 0.006; % Pixel size in meters
        end
        

        pcbLen = gridSize * pxSize + 1e-3; % PCB length
        pcbWid = gridSize * pxSize + 1e-3; % PCB width


        % Substrate setup
        d = dielectric('FR4');
        d.EpsilonR = er;
        d.Thickness = thick;

        % Ground plane setup
        GndPlane = antenna.Rectangle('Length', pcbLen, 'Width', pcbWid);

        % Top layer setup, initializing with a dummy rectangle
        r = antenna.Rectangle('Length', 1e-6, 'Width', 1e-5, 'Center', [0, 0]);

        
        disp(['startIndex: ', num2str(startIndex), ', endIndex: ', num2str(endIndex)]);

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
        xfeed = pxSize/2;
        yfeed = -gridSize * pxSize/2 + pxSize/3;

        p.FeedLocations = [xfeed, yfeed, 3, 1];

        % Uncomment the following lines to visualize the antenna
        
        %figure;
        %show(p);

        % Calculate S-parameters
        s_params = sparameters(p, freq);
        s11 = rfparam(s_params, 1, 1); % Extract S11 parameter

        % % % Calculate magnitude in dB
        S11_dB = mag2db(abs(s11));
        sparams_all(i,:) = S11_dB;

        % % % Uncomment the following lines to plot S-parameters
        %figure;
        %rfplot(s_params);
        %title(sprintf('S11 Plot for Antenna Design %d with feed at (%.3f, %.3f)', i, xfeed, yfeed));
        toc;
        
    end

    % Uncomment to show the final design
    % figure;
    % show(p);

    % Save S-parameters to a text file
    writematrix(sparams_all, 'sparameters.txt', 'Delimiter', 'tab');
end

    

