
suffixes = "!),.:;?]}¨·ˇˉ―‖’”…∶、。〃々〉》」』】〕〗！＂＇），．：；？］｀｜｝～￠"
prefixes = "([{·‘“〈《「『【〔〖（．［｛￡￥"


class WrapSession:

    line_width: int = 10

    def text_width(self, text: str) -> int:
        width = 0
        for char in text:
            if char.isascii():
                width += 1
            else:
                width += 2
        return width

    def group(self, text: str) -> list[str]:
        global suffixes, prefixes
        group_list: list[str] = []
        current_group: str = ""

        def append_to_group(text: str):
            nonlocal current_group
            current_group += text

        def last_char() -> str:
            return current_group[-1]

        def new_group():
            nonlocal current_group
            if current_group == "":
                return
            group_list.append(current_group)
            current_group = ""

        def type_sep(crt_char: str) -> bool:
            if len(current_group) == 0:
                return False
            # 中文转英文、中文转数字、英文转中文、数字转中文
            crt_type = crt_char.isascii()
            ls_type = last_char().isascii()

            return crt_type != ls_type

        for char in text:
            if char in prefixes:
                new_group()
                append_to_group(char)
            elif char in suffixes:
                append_to_group(char)
                new_group()
            # 是否是中文英文交界
            elif type_sep(char):
                new_group()
                append_to_group(char)
            elif char.isascii():
                append_to_group(char)
            else:
                if len(current_group) !=0 and last_char() not in prefixes:
                    new_group()
                append_to_group(char)

        new_group()
        return group_list
    
    def cut_left(self, text: str, width: int) -> tuple[str, str]:
        result = ""
        for char in text:
            if self.text_width(result + char) > width:
                break
            result += char
        return result, text[len(result):]
    
    def wrap(self, groups: list[str]) -> list[list[str]]:
        line_list: list[list[str]] = []
        current_line: list[str] = []
        current_width: int = 0

        def append_to_line(text: str):
            nonlocal current_line, current_width
            current_line.append(text)
            current_width += self.text_width(text)

        def new_line():
            nonlocal current_line, current_width
            line_list.append(current_line)
            current_line = []
            current_width = 0

        for group in groups:
            if group == '\n':
                new_line()
                continue

            if current_width + self.text_width(group) <= self.line_width:
                append_to_line(group)
            else:
                new_line()
                if self.text_width(group) <= self.line_width:
                    append_to_line(group)
                else:
                    while len(group) > 0:
                        left, group = self.cut_left(group, self.line_width)
                        append_to_line(left)
                        new_line()

        new_line()
        return line_list

    def process(self, text: str) -> list[list[str]]:
        
        groups = self.group(text)

        # print(groups)

        # group_widths = [self.text_width(group) for group in groups]

        # print(group_widths)

        lines = self.wrap(groups)

        # for line in lines:
        #     for group in line:
        #         print(group, end="")
        #     print()
        return lines
