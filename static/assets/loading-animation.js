const loadingAnimationHtml = `
    <div class="loading-container" style="--sphere-count:12">
        <style>
            .loading-container {
                width: 50dvw;
                aspect-ratio: 1;
                border-radius: 50%;
                position: absolute;
                transform: rotate(90deg);
                z-index: -1;
            }

            .sphere-handle {
                width: 50%;
                height: 1px;
                position: absolute;
                top: 50%;
                transform-origin: right center;
            }

            .sphere {
                width: 2dvw;
                aspect-ratio: 1;
                background-color: var(--col-4);
                border-radius: 50%;
            }

            .loading .loading-container {
                animation: rotate 30s forwards;

            }

            .loading .sphere-handle {
                animation: load 6s forwards;
            }

            @keyframes rotate {
                0% {
                    transform: rotate(90deg);
                }

                10% {
                    transform: rotate(270deg);
                }

                100% {
                    transform: rotate(450deg);
                }
            }

            @keyframes load {
                from {
                    transform: translateY(-100%) rotate(calc(0deg / var(--sphere-count) * var(--i)));
                }

                to {
                    transform: translateY(-100%) rotate(calc(360deg / var(--sphere-count) * var(--i)));
                }
            }
        </style>
        <div class="sphere-handle" style="--i:0">
            <div class="sphere"></div>
        </div>
        <div class="sphere-handle" style="--i:1">
            <div class="sphere"></div>
        </div>
        <div class="sphere-handle" style="--i:2">
            <div class="sphere"></div>
        </div>
        <div class="sphere-handle" style="--i:3">
            <div class="sphere"></div>
        </div>
        <div class="sphere-handle" style="--i:4">
            <div class="sphere"></div>
        </div>
        <div class="sphere-handle" style="--i:5">
            <div class="sphere"></div>
        </div>
        <div class="sphere-handle" style="--i:6">
            <div class="sphere"></div>
        </div>
        <div class="sphere-handle" style="--i:7">
            <div class="sphere"></div>
        </div>
        <div class="sphere-handle" style="--i:8">
            <div class="sphere"></div>
        </div>
        <div class="sphere-handle" style="--i:9">
            <div class="sphere"></div>
        </div>
        <div class="sphere-handle" style="--i:10">
            <div class="sphere"></div>
        </div>
        <div class="sphere-handle" style="--i:11">
            <div class="sphere"></div>
        </div>
    </div>
`