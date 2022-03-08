#ifndef __STD_STRING__
#define __STD_STRING__
#include <string>
#endif

#ifndef __STD_IOS__
#define __STD_IOS__
#include <ios>
#endif

#ifndef __STD_SSTREAM__
#define __STD_SSTREAM__
#include <sstream>
#endif

#ifndef __STD_IOMANIP__
#define __STD_IOMANIP__
#include <iomanip>
#endif

std::string two_digits_min(int d)
{
    std::ostringstream stream_obj;
    stream_obj << std::setw(2) << std::setfill('0') << d;
    return stream_obj.str();
}

std::string dec_places_min(double d, int places)
{
    std::ostringstream stream_obj;
    stream_obj << std::fixed << std::setprecision(places) << d;
    return stream_obj.str();
}