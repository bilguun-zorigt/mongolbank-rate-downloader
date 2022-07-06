#!/bin/bash

# install required packages
for REQUIRED_PKG in html-xml-utils #parallel
do
    PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
    # echo Checking for $REQUIRED_PKG: $PKG_OK
    if [ "" = "$PKG_OK" ]; then
    echo "No $REQUIRED_PKG. Setting up $REQUIRED_PKG."
    sudo apt-get --yes install $REQUIRED_PKG
    fi
done

function scrapeConcurrently {
    local dates="$1"

    mkdir -p .temp
    for date in $dates; do request $date & done
    wait
}

function request {
    local date="$1"

    local year=$(date -d "$date" +%Y)
    local month=$(date -d "$date" +%m)
    local day=$(date -d "$date" +%d)

	local urlParams="?vYear=$year&vMonth=$month&vDay=$day"
	local url="https://www.mongolbank.mn/dblistofficialdailyrate.aspx$urlParams"

    local doc=$(curl -s "$url" | hxnormalize -x)

	parse "$date" "$doc"
    printf "\033[44;34m█\033[0m"
}

function parse {
    local date="$1"
    local doc="$2"

	local spanIDPrefix="ContentPlaceHolder1_lbl"

    local elements=$(echo $doc | hxselect -s '\n' ".uk-comment-list span[id^=$spanIDPrefix]")

    old_IFS=$IFS; IFS=$'\n'
    rm -f ".temp/$date.txt"
    for element in $elements; do
        local spanId=$(echo $element | hxselect -c '::attr(id)')
        local symbol=${spanId//$spanIDPrefix/}

        local rate=$(echo $element | hxselect -c 'span')
        local rate=${rate//,/}
        echo "$symbol $rate" >> ".temp/$date.txt"
    done
    IFS=$old_IFS
}
