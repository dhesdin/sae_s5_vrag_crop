Models: qwen3-vl:8b-instruct embeddinggemma:latest
Image: dataset/market_0.jpg
Vector dimension: 768
Vector norm: 0.9999998787900486
Traceback (most recent call last):
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpx/_transports/default.py", line 101, in map_httpcore_exceptions
    yield
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpx/_transports/default.py", line 394, in handle_async_request
    resp = await self._pool.handle_async_request(req)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpcore/_async/connection_pool.py", line 256, in handle_async_request
    raise exc from None
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpcore/_async/connection_pool.py", line 236, in handle_async_request
    response = await connection.handle_async_request(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpcore/_async/connection.py", line 103, in handle_async_request
    return await self._connection.handle_async_request(request)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpcore/_async/http11.py", line 136, in handle_async_request
    raise exc
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpcore/_async/http11.py", line 106, in handle_async_request
    ) = await self._receive_response_headers(**kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpcore/_async/http11.py", line 177, in _receive_response_headers
    event = await self._receive_event(timeout=timeout)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpcore/_async/http11.py", line 217, in _receive_event
    data = await self._network_stream.read(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpcore/_backends/anyio.py", line 32, in read
    with map_exceptions(exc_map):
  File "/usr/lib/python3.12/contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpcore/_exceptions.py", line 14, in map_exceptions
    raise to_exc(exc) from exc
httpcore.ReadTimeout

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/valentin/Documents/sae_s5_vrag_crop/src/v_crop_rag/ollama_client/ollama_wrapper_iut.py", line 453, in _http_request_json
    response = await client.request(
               ^^^^^^^^^^^^^^^^^^^^^
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpx/_client.py", line 1540, in request
    return await self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpx/_client.py", line 1629, in send
    response = await self._send_handling_auth(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpx/_client.py", line 1657, in _send_handling_auth
    response = await self._send_handling_redirects(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpx/_client.py", line 1694, in _send_handling_redirects
    response = await self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpx/_client.py", line 1730, in _send_single_request
    response = await transport.handle_async_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpx/_transports/default.py", line 393, in handle_async_request
    with map_httpcore_exceptions():
  File "/usr/lib/python3.12/contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "/home/valentin/Documents/sae_s5_vrag_crop/.venv/lib/python3.12/site-packages/httpx/_transports/default.py", line 118, in map_httpcore_exceptions
    raise mapped_exc(message) from exc
httpx.ReadTimeout

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/valentin/Documents/sae_s5_vrag_crop/scripts/manual_index_test.py", line 67, in <module>
    asyncio.run(main())
  File "/usr/lib/python3.12/asyncio/runners.py", line 194, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/base_events.py", line 687, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/home/valentin/Documents/sae_s5_vrag_crop/scripts/manual_index_test.py", line 51, in main
    raw_response = await vlm.generate(prompt=build_extraction_prompt(), image=IMAGE_PATH)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/valentin/Documents/sae_s5_vrag_crop/src/v_crop_rag/ollama_client/vlm.py", line 30, in generate
    result = await self._client.generate_with_image(model=self._model, prompt=prompt, image=image)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/valentin/Documents/sae_s5_vrag_crop/src/v_crop_rag/ollama_client/ollama_wrapper_iut.py", line 375, in generate_with_image
    payload = await self._http_request_json("POST", "/api/generate", body=body)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/valentin/Documents/sae_s5_vrag_crop/src/v_crop_rag/ollama_client/ollama_wrapper_iut.py", line 466, in _http_request_json
    raise OllamaConnectionError(f"Impossible de joindre Ollama à {url}: {e}") from e
v_crop_rag.ollama_client.ollama_wrapper_iut.OllamaConnectionError: Impossible de joindre Ollama à http://10.22.28.190:11434/api/generate: 
