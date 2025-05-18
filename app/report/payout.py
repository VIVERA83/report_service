from collections import defaultdict

from icecream import ic

from app.report.base import BaseReport


class Payout(BaseReport):

    def get_report(
            self,
            columns: dict[str, str] = None,
            subtotal_columns: list[str] = None,
            group: str = None,
    ) -> dict:
        if columns is None:
            columns = {key : key for key in self.dc.__annotations__.keys()}
        if group:
            columns = {group: group, **columns}

        self._update_column_widths(columns)
        self.subtotal_columns = subtotal_columns if subtotal_columns else []
        self.group = group if group is not None else ""
        self.sort_records(*columns.keys())
        report = self.create_json_report(list(columns.keys()))
        self._show_report(columns)
        return report

    def create_json_report(self, columns: list[str]) -> dict:
        report = defaultdict(dict)
        for record in self._records:
            atr = getattr(record, self.group or "", "")
            if not report[atr].get("items"):
                report[atr]["items"] = [
                    self._sort_raw_record(record.as_dict(*columns), columns)
                ]
                for column in self.subtotal_columns:
                    report[atr][column] = getattr(record, column)
            else:
                report[atr]["items"].append(
                    self._sort_raw_record(record.as_dict(*columns), columns)
                )
                for column in self.subtotal_columns:
                    report[atr][column] += getattr(record, column)

        return report

    def _get_title_report(self, columns: dict[str, str] = None) -> str:
        if columns is None:
            columns = self.__get_columns()

        title = ""
        for column_name, new_name in columns.items():
            title += " " * self.indent
            title += new_name.rjust(self._max_lens[column_name])
        return title

    def __get_columns(self) -> dict[str, str]:
        return {field: field for field in self._records[0].__annotations__.keys()}

    def _show_report(
            self,
            columns: dict[str, str] = None,
    ) -> None:

        result: list[str] = [self._get_title_report(columns)]
        self.current_group = ""
        self.subtotal: dict[str, dict[str, int]] = defaultdict(dict)
        self.is_new_group = True

        for record in self._records:
            raw_record = self._sort_raw_record(
                record.as_dict(*columns.keys()), [*columns.keys()]
            )
            main_line = self.__get_update_main_line(raw_record, columns)
            group_line = self.__get_update_group_line(raw_record)
            sub_line = self.__get_update_sub_line(raw_record)
            self.__update_subtotal(raw_record)

            if sub_line:
                result.append(sub_line)
            if group_line:
                result.append(group_line)

            result.append(main_line)
        #
        self.is_new_group = True
        sub_line = self.__get_update_sub_line(self._records[0].as_dict(*columns.keys()))
        result.append(sub_line)
        return print(*result, sep="\n")

    def __get_update_main_line(
            self, record: dict[str, int | str], column: dict[str, str]
    ) -> str:
        line = " " * self.indent
        for key, value in record.items():
            if column[key] == " ":
                line += "_" * self._max_lens[key]
            else:
                line += str(value).ljust(self._max_lens[key])
            line += " " * self.indent
        return line

    def __get_update_group_line(self, record: dict[str, int | str]) -> str:
        if value := record.get(self.group):
            if self.current_group != value:
                self.current_group = value
                self.is_new_group = True
                return " " * self.indent + str(self.current_group)
        return ""

    def __get_update_sub_line(self, record: dict[str, int | str]) -> str:
        if self.is_new_group and len(self.subtotal) > 0:
            self.is_new_group = False
            line = " " * self.indent
            sub_total = [*self.subtotal.values()][-1]
            for key in record.keys():
                if key in self.subtotal_columns:
                    line += str(sub_total[key]).ljust(self._max_lens[key])
                else:
                    line += " " * self._max_lens[key]
                line += " " * self.indent
            return line
        self.is_new_group = False
        return ""

    def __update_subtotal(self, record: dict[str, int | str]):
        for key, value in record.items():
            if key in self.subtotal_columns:
                if not self.subtotal.get(self.current_group):
                    self.subtotal[self.current_group] = defaultdict(int)
                self.subtotal[self.current_group][key] += value

    @staticmethod
    def _sort_raw_record(raw_record: dict, sort_columns: list[str]) -> dict[str, str]:
        sorting_rule = lambda el: sort_columns.index(el[0])
        return {
            key: value for key, value in sorted(raw_record.items(), key=sorting_rule)
        }
