import LocalTime from "local-time";

LocalTime.config.i18n["ca"] = {
  date: {
    dayNames: ["Diumenge", "Dilluns", "Dimarts", "Dimecres", "Dijous", "Divendres", "Dissabte"],
    abbrDayNames: ["Dg.", "Dl.", "Dt.", "Dc.", "Dj.", "Dv.", "Ds."],
    monthNames: ["Gener", "Febrer", "Març", "Abril", "Maig", "Juny", "Juliol", "Agos", "Setembre", "Octubre", "Novembre", "Desembre"],
    abbrMonthNames: ["Gen.", "Febr.", "Març", "Abr.", "Maig", "Juny", "Jul.", "Ag.", "Set.", "Oct.", "Nov.", "Des."],
    yesterday: "ahir",
    today: "avui",
    tomorrow: "demà",
    on: "el {date}",
    formats: {
      default: "%e %B, %Y",
      thisYear: "%e %B"
    }
  },
  time: {
    am: "",
    pm: "",
    singular: "un {time}",
    singularAn: "una {time}",
    elapsed: "fa {time}",
    second: "segon",
    seconds: "segons",
    minute: "minut",
    minutes: "minuts",
    hour: "hora",
    hours: "hores",
    formats: {
      default: "%H:%M"
    }
  },
  datetime: {
    at: "el {date} a les {time}",
    formats: {
      default: "%e %B %Y, %H:%M"
    }
  }
};
