import * as bootstrap from "bootstrap";
import LocalTime from "local-time";

import "./i18n";
import "./controllers";
import "../../../scorecard/static/scorecard/functions";

document.addEventListener("DOMContentLoaded", function () {
  LocalTime.config.locale = document.documentElement.lang;
  LocalTime.start();
});
