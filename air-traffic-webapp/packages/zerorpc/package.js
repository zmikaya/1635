Package.describe({
  summary: 'Wraps the zerorpc module from Npm in a fiber.',
  version: '0.2.0',
  name: 'kelvinly:zerorpc',
  // Brief, one-line summary of the package.
  // URL to the Git repository containing the source code for this package.
  git: 'https://github.com/ycliuhw/zerorpc.git',
  // By default, Meteor will default to using README.md for documentation.
  // To avoid submitting documentation, set this field to null.
  documentation: 'README.md'
});

Npm.depends({
    zerorpc: "0.9.5",
    fibers: "1.0.5"
});

Package.onUse(function(api) {
  // If no version is specified for an 'api.use' dependency, use the
  // one defined in Meteor 0.9.0.
  // api.versionsFrom('1.1.0.2');
  api.use('ecmascript@0.1.4');
  api.addFiles('zerorpc.js', 'server');
  api.export("Zerorpc", "server");
});

Package.onTest(function(api) {
  api.use('tinytest');
  api.use('kelvinly:zerorpc');
  api.addFiles('zerorpc-tests.js');
});
