const { chalk } = require("@vue/cli-shared-utils");
const lint = require("../lint");

const styleLint = {
  stylelint: "^14.2.0",
  'postcss-html': '^1.3.0'
};

const styleLintScss = {
  "stylelint-config-recommended-scss": "^5.0.0",
};

const styleLintRecommended = {
  "stylelint-config-recommended-vue": "^1.1.0",
};

const styleLintPrettier = {
  "stylelint-config-prettier": "^9.0.3",
  "stylelint-prettier": "^2.0.0",
  prettier: "^2.4.1",
};

const lintStaged = {
  "lint-staged": "^12.0.0",
};

module.exports = (api, options = {}) => {
  const { overwriteConfig } = options;
  if (overwriteConfig === "abort") {
    api.exitLog(chalk`{yellow Plugin setup successfully cancelled}`, "warn");
    return;
  }

  let { lintStyleOn = [] } = options;
  if (typeof lintStyleOn === "string") {
    lintStyleOn = lintStyleOn.split(",");
  }

  const pkg = {
    scripts: {
      "lint:style": "vue-cli-service lint:style",
    },
    devDependencies: {
      ...styleLint,
    },
    vue: {
      pluginOptions: {
        lintStyleOnBuild: lintStyleOn.includes("build"),
        stylelint: {},
      },
    },
    stylelint: {
      root: true,
      extends: [],
    },
  };

  const { config, scss } = options;

  if (scss) {
    pkg.stylelint.extends.push("stylelint-config-recommended-scss");
    Object.assign(pkg.devDependencies, {
      ...styleLintScss,
    });
  }

  if (config === "recommended") {
    pkg.stylelint.extends.push("stylelint-config-recommended-vue" + (scss ? '/scss' : ''));
    Object.assign(pkg.devDependencies, {
      ...styleLintRecommended,
    });
  } else if (config === "prettier") {
    pkg.stylelint.extends.push("stylelint-config-recommended-vue" + (scss ? '/scss' : ''));
    pkg.stylelint.extends.push("stylelint-prettier/recommended");
    Object.assign(pkg.devDependencies, {
      ...styleLintRecommended,
      ...styleLintPrettier,
    });
  }

  if (lintStyleOn.includes("commit")) {
    Object.assign(pkg.devDependencies, {
      ...lintStaged,
    });
    pkg.gitHooks = {
      "pre-commit": "lint-staged",
    };
    pkg["lint-staged"] = {
      "*.{vue,htm,html,css,sss,less,scss}": [
        "vue-cli-service lint:style",
      ],
    };
  }

  api.render("./template");
  api.addConfigTransform("stylelint", {
    file: {
      js: [".stylelintrc.js", "stylelint.config.js"],
      json: [".stylelintrc", ".stylelintrc.json"],
      yaml: [".stylelintrc.yaml", ".stylelintrc.yml"],
    },
  });
  api.extendPackage(pkg);

  api.onCreateComplete(async () => {
    await lint(api, { silent: true });
  });
};
