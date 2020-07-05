const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {

    entry: ['./react/index.js'],
    output: {
        filename: 'build.js',
        path: path.join(__dirname, 'flask/static/'),
    },
    resolve: {
        extensions: ['.js', '.jsx'],
    },
    module: {
        rules: [
        {
            test: /\.(js|jsx)$/,
            exclude: /node_modules/,
            use: ['babel-loader']
        },     
        ]
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './react/index.html',
            filename: "index.html",
            inject: false,
    }),
    ]

}
    