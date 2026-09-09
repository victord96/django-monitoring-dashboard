import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  static values = {
    param: { type: String, default: "page" },
    page: Number
  };

  connect() {
    const url = new URL(window.location.href);
    url.searchParams.set(this.paramValue, this.pageValue);
    this.element.href = url.href;
  }
}
