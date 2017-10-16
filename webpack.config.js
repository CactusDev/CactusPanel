module.exports = {
    entry: "./src/index.tsx",
    output: {
        filename: "bundle.js",
        path: __dirname + "/dist"
    },

    devtool: "source-map",

    resolve: {
        extensions: [".ts", ".tsx", ".js", ".json"]
    },

    module: {
        rules: [
            { test: /\.tsx?$/, loader: "awesome-typescript-loader" },
            { enforce: "pre", test: /\.js$/, loader: "source-map-loader" },
            {
                test: /\.css$/,
                use: [
                  "style-loader",
                  {
                    loader: "css-loader",
                    options: {
                      modules: true,
                      sourceMap: true,
                      importLoaders: 1,
                      localIdentName: "[name]--[local]--[hash:base64:8]"
                    }
                  },
                  "postcss-loader"
                ]
              }
        ]
    },

    externals: {
        "react": "React",
        "react-dom": "ReactDOM"
    },
};