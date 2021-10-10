.. -*- fill-column: 79; mode: rst; eval: (flyspell-mode) -*-

=========================================
CaPython - Python interpreter for Camunda
=========================================

.. |const_entrypoint| replace:: ``python``

Joining Camunda and Python gives an ordinary Camunda scripting user **a way**
more freedom than just utilizing the alternatives such as:

.. |nashorn| replace:: Nashorn
.. _nashorn: https://github.com/openjdk/nashorn
.. _nash_rem: https://stackoverflow.com/a/65265993/5994041
.. |groovy| replace:: Groovy
.. _groovy: https://groovy-lang.org
.. |jsr223| replace:: JSR 223
.. _jsr223: https://en.wikipedia.org/wiki/Scripting_for_the_Java_Platform
.. |forof| replace:: ``for...of``
.. _forof:
   https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...of

#. Writing the logic in Java, compiling and embedding into Camunda's image
#. Utilizing present engines such as:

   * |nashorn|_ - which still lives in the age where even |forof|_ is
     non-existent (`and has been removed anyway <nash_rem_>`__)
   * |groovy|_ - which feels like "Java meets Bash" but still drags along the
     unreadability and unnecessary robustness for the use-case of *scripting* a
     task
   * others defined in |jsr223|_

#. Hoping for the Jython integration, which nevertheless still require you to
   bring custom JARs and ensure it doesn't break your Camunda engine along the
   way when something upgrades

.. |kapitan| replace:: [ka.piˈt̪ãn]
.. _kapitan: https://en.wiktionary.org/wiki/capit%C3%A1n#Spanish

Meet CaPython (|kapitan|_), joining the pleasant experience from Camunda
orchestration layer and bringing to you the way of scripting that doesn't
require you to question own sanity in the process.

.. |monolith| replace:: Monolithic application
.. _monolith: https://en.wikipedia.org/wiki/Monolithic_application

CaPython is going to take you on the journey in the insane seas of
strict-typing for scripting and gluing JARs on top of already complex engine
(a.k.a. creating a |monolith|_) by utilizing two simple concepts under the hood:

.. |camrest| replace:: Camunda REST API
.. _camrest: https://docs.camunda.org/manual/latest/reference/rest/
.. |camcom| replace:: https://github.com/camunda-community-hub
.. |cametcpy| replace:: Camunda External Task Client in Python
.. _cametcpy: |camcom|/camunda-external-task-client-python3
.. |exec| replace:: ``exec()``
.. _exec: https://docs.python.org/3/library/functions.html#exec

#. the good old |camrest|_ via |cametcpy|_
#. the even older and even better, |exec|_

Disregard anything scary you've read about ``eval()`` / |exec|_ functions. In
this case |exec|_ is the perfect tool because you'll be executing a custom code
anyway and it's up to **you** to secure the execution access prior the flow
even reaching any |exec|_ or similar functionality.

*However!* As with any piece of software, even this can be misused, therefore
be aware of the entrypoint variable (called |const_entrypoint| by default) and
ensure **nothing** from the outside of the process is passed into it. Even
though it's dockerized and silly ``rm -rf /`` attempts won't do a real harm,
this is a way for an attacker to basically hijack your Python
interpreter by inserting malicious code instead of, or appended to yours.
Then, based on the environment you prepare, an attacker can:

.. |fork| replace:: Fork-bomb
.. _fork: https://en.wikipedia.org/wiki/Fork_bomb

* create a |fork|_ just to make your container eat more resources, therefore
  money, if you pay for the deployment
* utilize the CPU/GPU for processing (miners are trendy nowadays)
* read/write to the container's filesystem (and **anything** mounted to it)
* reach the network (and anything that's in it) container is deployed on
* reach the network (and anything that's in it) pod is deployed on (if using
  Kubernetes)
* reach the Internet and depending on the networking rules upload and/or
  download content
* execute anything present or downloaded into the container
* access Camunda via its API

.. _ripley_nuke: https://www.youtube.com/watch?v=aCbfMkh940Q

That being said, the same applies to any other scripting engine in Camunda
including the existing ones, therefore if you have already ignored these points
successfully, your system either already has hole(s) in it or might have been
compromised. Depending on your scenario, `this might be appropriate
<ripley_nuke_>`__.
