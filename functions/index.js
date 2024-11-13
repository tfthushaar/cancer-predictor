const functions = require('firebase-functions');
const express = require('express');
const app = express();

exports.app = functions.https.onRequest(app);