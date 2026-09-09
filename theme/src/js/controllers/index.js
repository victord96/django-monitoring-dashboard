import { Application } from "@hotwired/stimulus";

import PaginationLinkController from "./pagination_link_controller.js";

const application = Application.start();
application.register("pagination-link", PaginationLinkController);
