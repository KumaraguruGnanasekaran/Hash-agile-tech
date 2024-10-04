function longPali(s) {
    var start = 0;
    var maxLength = 1;
    function eac(left, right) {
        while (left >= 0 && right < s.length && s[left] === s[right]) {
            if (right - left + 1 > maxLength) {
                start = left;
                maxLength = right - left + 1;
            }
            left--;
            right++;
        }
    }
    for (var i = 0; i < s.length; i++) {
        eac(i, i);
        eac(i, i + 1);
    }
    var result = '';
    for (var i = start; i < start + maxLength; i++) {
        result += s[i];
    }
    return result;
}
var input = "babad";
var input2 = "noonabcba";
var input3 = "malayalam";
console.log(longPali(input));
console.log(longPali(input2));
console.log(longPali(input3));
