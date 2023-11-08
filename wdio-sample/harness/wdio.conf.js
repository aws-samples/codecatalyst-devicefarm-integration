const { launcher } = require("wdio-aws-device-farm-service");

exports.config = {
    runner: "local",
    specs: [
        "tests/**/*.test.js"
    ],
    maxInstances: 4,
    capabilities: [
        {
            browserName: 'chrome',
            acceptInsecureCerts: true,
        },
        {
            browserName: 'firefox',
            acceptInsecureCerts: true,
        }
    ],
    logLevel: "trace",
    framework: "mocha",
    outputDir: __dirname,
    reporters: ["spec"],
    mochaOpts: {
        ui: 'bdd',
        timeout: 30000,
    },
    services: [
        [
            launcher,
            {
                projectArn: process.env.PROJECT_ARN
            },
        ],
    ],
    reporters: [
        'dot',
        ['junit', {
            outputDir: './',
            outputFileFormat: function(options) { // optional
                return `results-${options.cid}.${options.capabilities}.xml`
            }
        }]
    ]
}
