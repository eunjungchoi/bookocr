module.exports = {
  "extends": [
    "eslint:recommended"
  ],
  "parser": "babel-eslint",
  "parserOptions": {
    "ecmaVersion": 6,
    "sourceType": "module",
    "ecmaFeatures": {
      "classes": true,
      "experimentalObjectRestSpread": true
    }
  },
  "env": {
    "browser": true
  },
  "globals": {
	"$": true,
	"ejs": true,
	"xport": true,
	"equire": true
  },
  "rules": {
    "indent": ["warn", 2],
    "no-var": 0,
    "vars-on-top": 0,
    "camelcase": 0,
    "prefer-arrow-callback": 0,
    "no-use-before-define": 0,
    "semi": ["error", "always"],
  }
};

