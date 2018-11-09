GPROF_FILE=${1}

echo "%TIME"
grep -m1 "SmdReader::get(unsigned int)" ${GPROF_FILE} | awk '{print $1}'
grep -m1 "std::vector<std::shared_ptr<Buffer>, std::allocator<std::shared_ptr<Buffer> > >::operator" ${GPROF_FILE} | awk '{print $1}'
grep -m1 "std::__shared_ptr_access<Buffer, (__gnu_cxx::_Lock_policy)2, false, false>::operator->() const" ${GPROF_FILE} | awk '{print $1}'
grep -m1 "std::__shared_ptr<Buffer, (__gnu_cxx::_Lock_policy)2>::get() const" ${GPROF_FILE} | awk '{print $1}'
grep -m1 "std::__shared_ptr_access<Buffer, (__gnu_cxx::_Lock_policy)2, false, false>::_M_get() const" ${GPROF_FILE} | awk '{print $1}'
grep -m1 "Buffer::read_partial()" ${GPROF_FILE} | awk '{print $1}'
grep -m1 "SmdReader::get_payload" ${GPROF_FILE} | awk '{print $1}'
grep -m1 "SmdReader::get_dgram" ${GPROF_FILE} | awk '{print $1}'

echo "TIME(s)"
grep -m1 "SmdReader::get(unsigned int)" ${GPROF_FILE} | awk '{print $3}'
grep -m1 "std::vector<std::shared_ptr<Buffer>, std::allocator<std::shared_ptr<Buffer> > >::operator" ${GPROF_FILE} | awk '{print $3}'
grep -m1 "std::__shared_ptr_access<Buffer, (__gnu_cxx::_Lock_policy)2, false, false>::operator->() const" ${GPROF_FILE} | awk '{print $3}'
grep -m1 "std::__shared_ptr<Buffer, (__gnu_cxx::_Lock_policy)2>::get() const" ${GPROF_FILE} | awk '{print $3}'
grep -m1 "std::__shared_ptr_access<Buffer, (__gnu_cxx::_Lock_policy)2, false, false>::_M_get() const" ${GPROF_FILE} | awk '{print $3}'
grep -m1 "Buffer::read_partial()" ${GPROF_FILE} | awk '{print $3}'
grep -m1 "SmdReader::get_payload" ${GPROF_FILE} | awk '{print $3}'
grep -m1 "SmdReader::get_dgram" ${GPROF_FILE} | awk '{print $3}'

echo "CALLS"
grep -m1 "SmdReader::get(unsigned int)" ${GPROF_FILE} | awk '{print $4}'
grep -m1 "std::vector<std::shared_ptr<Buffer>, std::allocator<std::shared_ptr<Buffer> > >::operator" ${GPROF_FILE} | awk '{print $4}'
grep -m1 "std::__shared_ptr_access<Buffer, (__gnu_cxx::_Lock_policy)2, false, false>::operator->() const" ${GPROF_FILE} | awk '{print $4}'
grep -m1 "std::__shared_ptr<Buffer, (__gnu_cxx::_Lock_policy)2>::get() const" ${GPROF_FILE} | awk '{print $4}'
grep -m1 "std::__shared_ptr_access<Buffer, (__gnu_cxx::_Lock_policy)2, false, false>::_M_get() const" ${GPROF_FILE} | awk '{print $4}'
grep -m1 "Buffer::read_partial()" ${GPROF_FILE} | awk '{print $4}'
grep -m1 "SmdReader::get_payload" ${GPROF_FILE} | awk '{print $4}'
grep -m1 "SmdReader::get_dgram" ${GPROF_FILE} | awk '{print $4}'

