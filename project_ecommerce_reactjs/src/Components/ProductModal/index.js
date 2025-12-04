import Dialog from '@mui/material/Dialog';
import { MdClose } from "react-icons/md";
import Button from '@mui/material/Button'
import Rating from '@mui/material/Rating';
import Slider from "react-slick"
const ProductModal = (props) => {

    const zoomSliderBig = useRef()
    return (
        <>
            <Dialog open={true} className="productModal" onClose={() => props.closeProductModal()}>
                <Button className='close_' onClick={() => props.closeProductModal()} ><MdClose /></Button>
                <h4 class="mb-1 font-weight-bold">All Natural Chicken</h4>
                <div className='d-flex align-item-center'>
                    <div className='d-flex align-item-center mr-4'>
                        <span>Brands</span>
                        <span className='ml-2'><b>Welch's</b></span>
                    </div>

                    <Rating name="read-only" value={5} size="small" precision={0.5} readOnly />
                    


                </div>

                <hr />



                <div className='row mt-2 productDetailModal'>
                    <div className='col-md-5'>
                        <Slider {...settings2} className='zoomSliderBig' ref={zoomSliderBig}>
                            {
                                currentProduct.productImages !== undefined && currentProduct.productImages.map((imgUrl, index) => {
                                    return (
                                        <div className='item'>
                                            <InnerImageZoom
                                                zoomType="hover" zoomScale={1}
                                                src={`https://klbtheme.com/bacola/wp-content/uploads/2021/04/product-image-62.jpg`} />
                                        </div>
                                    )
                                })
                            }
                        </Slider>
                    </div>

                    <div className='col-md-7'>

                    </div>
                </div>

            </Dialog>
        </>

    )

}

export default ProductModal;
/*
<Slider {...settings2} className='zoomSliderBig' ref={zoomSliderBig}>
    {
        currentProduct.productImages !== undefined && currentProduct.productImages.map((imgUrl, index) => {
            return (
                <div className='item'>
                    <InnerImageZoom
                        zoomType="hover" zoomScale={1}
                        src={`${imgUrl}?im=Resize=(${bigImageSize[0]},${bigImageSize[1]})`} />
                </div>
            )
        })
    }
</Slider>
*/