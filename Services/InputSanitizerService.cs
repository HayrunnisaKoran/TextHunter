using System.Net;
using System.Text.RegularExpressions;

namespace TextHunter.Services
{
    public class InputSanitizerService: IInputSanitizerService
    {
        public string Sanitize(string input)
        {
            if (string.IsNullOrWhiteSpace(input))
                return input;

            // html etıketlerını kaldır
            string cleaned = Regex.Replace(input, "<.*>", string.Empty);

            //kalan karakterlerı html encode yap
            return WebUtility.HtmlEncode(cleaned);
        }

    }
}
