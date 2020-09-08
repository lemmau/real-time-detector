const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: ['@babel/polyfill', './react/index.js'],
    output: {
        filename: 'build.js',
        path: path.join(__dirname, 'flask/static/'),
        publicPath: '/',
    },
    resolve: {
        extensions: ['.js', '.jsx'],
    },
    module: {
        rules: [
        {
            test: /\.m?js$/,
            use: {
                loader: 'babel-loader',
                options: {
                presets: ['@babel/preset-env', '@babel/preset-react']
                }
            }
        },
        {
            test: /\.s[ac]ss$/i,
            use: [
              // Creates `style` nodes from JS strings
              'style-loader',
              // Translates CSS into CommonJS
              'css-loader',
              // Compiles Sass to CSS
              'sass-loader',
            ],
        },      
        {
            test: /\.css$/i,
            use: ['css-loader'],
        },
        {
            test: /\.(png|svg|jpg|gif)$/,
            use: [
            'file-loader',
            ],
        },
        ]
    },
    devServer: {
        historyApiFallback: true,
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './react/index.html',
            filename: "index.html",
    }),
    ],
    externals: {
        'Config': JSON.stringify(require(path.join(__dirname, 'config/config.json'))),
    },
}
