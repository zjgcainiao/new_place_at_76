!function(e){function n(e){return RegExp("(\\()(?:"+e+")(?=[\\s\\)])")}function a(e){return RegExp("([\\s([])(?:"+e+")(?=[\\s)])")}var t="(?!\\d)[-+*/~!@$%^=<>{}\\w]+",r="(\\()",i="(?=\\s)",s="(?:[^()]|\\((?:[^()]|\\((?:[^()]|\\((?:[^()]|\\((?:[^()]|\\([^()]*\\))*\\))*\\))*\\))*\\))*",l={heading:{pattern:/;;;.*/,alias:["comment","title"]},comment:/;.*/,string:{pattern:/"(?:[^"\\]|\\.)*"/,greedy:!0,inside:{argument:/[-A-Z]+(?=[.,\s])/,symbol:RegExp("`"+t+"'")}},"quoted-symbol":{pattern:RegExp("#?'"+t),alias:["variable","symbol"]},"lisp-property":{pattern:RegExp(":"+t),alias:"property"},splice:{pattern:RegExp(",@?"+t),alias:["symbol","variable"]},keyword:[{pattern:RegExp(r+"(?:and|(?:cl-)?letf|cl-loop|cond|cons|error|if|(?:lexical-)?let\\*?|message|not|null|or|provide|require|setq|unless|use-package|when|while)"+i),lookbehind:!0},{pattern:RegExp(r+"(?:append|by|collect|concat|do|finally|for|in|return)"+i),lookbehind:!0}],declare:{pattern:n("declare"),lookbehind:!0,alias:"keyword"},interactive:{pattern:n("interactive"),lookbehind:!0,alias:"keyword"},boolean:{pattern:a("nil|t"),lookbehind:!0},number:{pattern:a("[-+]?\\d+(?:\\.\\d*)?"),lookbehind:!0},defvar:{pattern:RegExp(r+"def(?:const|custom|group|var)\\s+"+t),lookbehind:!0,inside:{keyword:/^def[a-z]+/,variable:RegExp(t)}},defun:{pattern:RegExp(r+"(?:cl-)?(?:defmacro|defun\\*?)\\s+"+t+"\\s+\\("+s+"\\)"),lookbehind:!0,greedy:!0,inside:{keyword:/^(?:cl-)?def\S+/,arguments:null,function:{pattern:RegExp("(^\\s)"+t),lookbehind:!0},punctuation:/[()]/}},lambda:{pattern:RegExp(r+"lambda\\s+\\(\\s*(?:&?"+t+"(?:\\s+&?"+t+")*\\s*)?\\)"),lookbehind:!0,greedy:!0,inside:{keyword:/^lambda/,arguments:null,punctuation:/[()]/}},car:{pattern:RegExp(r+t),lookbehind:!0},punctuation:[/(?:['`,]?\(|[)\[\]])/,{pattern:/(\s)\.(?=\s)/,lookbehind:!0}]},o={"lisp-marker":RegExp("&(?!\\d)[-+*/~!@$%^=<>{}\\w]+"),varform:{pattern:RegExp("\\("+t+"\\s+(?=\\S)"+s+"\\)"),inside:l},argument:{pattern:RegExp("(^|[\\s(])"+t),lookbehind:!0,alias:"variable"},rest:l},p="\\S+(?:\\s+\\S+)*",d={pattern:RegExp(r+s+"(?=\\))"),lookbehind:!0,inside:{"rest-vars":{pattern:RegExp("&(?:body|rest)\\s+"+p),inside:o},"other-marker-vars":{pattern:RegExp("&(?:aux|optional)\\s+"+p),inside:o},keys:{pattern:RegExp("&key\\s+"+p+"(?:\\s+&allow-other-keys)?"),inside:o},argument:{pattern:RegExp(t),alias:"variable"},punctuation:/[()]/}};l.lambda.inside.arguments=d,l.defun.inside.arguments=e.util.clone(d),l.defun.inside.arguments.inside.sublist=d,e.languages.lisp=l,e.languages.elisp=l,e.languages.emacs=l,e.languages["emacs-lisp"]=l}(Prism);